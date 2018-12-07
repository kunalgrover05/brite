# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView

from core.models import InsuranceForm, DataField, EnumChoice


class EnumChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnumChoice
        fields = '__all__'


class FieldSerializer(serializers.ModelSerializer):
    enum_choices = EnumChoiceSerializer(many=True)
    class Meta:
        model = DataField
        fields = '__all__'


class InsuranceSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True)
    class Meta:
        model = InsuranceForm
        fields = '__all__'


class InsuranceFieldsView(ListAPIView, RetrieveAPIView):
    serializer_class = InsuranceSerializer
    queryset = InsuranceForm.objects.all()

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk', None):
            return self.retrieve(request, args, kwargs)
        else:
            return self.list(request, args, kwargs)