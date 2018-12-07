# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from core.models import DataField, EnumChoice, FieldType
from userdata.models import DataFieldValue, UserInsuranceFormDetail


class DataFieldValueSerializer(serializers.ModelSerializer):
    fieldId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=DataField.objects.all(), source='field')
    userInsuranceFormDetail = serializers.PrimaryKeyRelatedField(write_only=True,
                                                                 queryset=UserInsuranceFormDetail.objects.all(),
                                                                 required=False)
    field = serializers.StringRelatedField(source='field.name', read_only=True)
    value = serializers.CharField()

    def validate(self, attrs):
        validated_data = super(DataFieldValueSerializer, self).validate(attrs)

        if validated_data['field'].type == FieldType.NUMBER:
            validated_data['value'] = serializers.FloatField().to_internal_value(validated_data['value'])
        elif validated_data['field'].type == FieldType.DATE:
            validated_data['value'] = serializers.DateField(input_formats=['iso-8601']).to_internal_value(validated_data['value'])
        elif validated_data['field'].type == FieldType.ENUM:
            validated_data['value'] = serializers.PrimaryKeyRelatedField(queryset=EnumChoice.objects.all())\
                                            .to_internal_value(validated_data['value'])

        DataFieldValue.validate(validated_data['field'], validated_data['value'])

        return validated_data

    def create(self, validated_data):
        fieldData = DataFieldValue.create(self.validated_data['field'], self.validated_data['value'],
                                          self.validated_data['userInsuranceFormDetail'])
        return fieldData

    class Meta:
        model = DataFieldValue
        fields = ('field', 'value', 'fieldId', 'userInsuranceFormDetail')


class UserDataSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    dataFieldValues = DataFieldValueSerializer(many=True)
    insuranceName = serializers.StringRelatedField(source='insurance.name', read_only=True)

    def validate(self, attrs):
        # Verify that all the insurance fields are present in this API.
        validated_data = super(UserDataSerializer, self).validate(attrs)

        fields = validated_data['dataFieldValues']
        for field in validated_data['insurance'].fields.all():
            found = False
            for field_validated in fields:
                if field_validated['field'] == field:
                    found = True

            if not found:
                raise ValidationError("Field missing:" + str(field))

        if len(validated_data['insurance'].fields.all()) != len(fields):
            raise ValidationError("Extra fields found")

        return validated_data

    def create(self, validated_data):
        validated_data.pop('dataFieldValues', [])

        instance = UserInsuranceFormDetail()
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        field_objs = []

        for field in self.initial_data['dataFieldValues']:
            field['userInsuranceFormDetail'] = instance.pk
            field_serialized = DataFieldValueSerializer(data=field)
            if field_serialized.is_valid():
                field_serialized.save()
                field_objs.append(field_serialized.instance)
            else:
                raise ValidationError(field_serialized.errors)

        return instance

    class Meta:
        model = UserInsuranceFormDetail
        fields = ('dataFieldValues', 'insurance', 'user', 'id', 'insuranceName')

class UserDataView(ListAPIView, RetrieveAPIView, CreateAPIView):
    serializer_class = UserDataSerializer
    queryset = UserInsuranceFormDetail.objects.all()

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk', None):
            return self.retrieve(request, args, kwargs)
        else:
            return self.list(request, args, kwargs)