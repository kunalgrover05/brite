# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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


class InsuranceFieldsView(ListAPIView):
    """
    get: List all Insurance forms created
    """
    serializer_class = InsuranceSerializer
    queryset = InsuranceForm.objects.all()

class InsuranceFieldView(RetrieveAPIView):
    """
    get: Retrieve details for a single Insurance form
    """
    serializer_class = InsuranceSerializer
    queryset = InsuranceForm.objects.all()