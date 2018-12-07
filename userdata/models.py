# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import numbers
import datetime
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from core.models import DataField, EnumChoice, InsuranceForm, FieldType


class DataFieldValue(models.Model):
    field = models.ForeignKey(DataField)
    char_val = models.CharField(max_length=190, null=True, blank=True)
    date_val = models.DateField(null=True, blank=True)
    number_val = models.IntegerField(null=True, blank=True)
    enum_val = models.ForeignKey(EnumChoice, null=True, blank=True)
    userInsuranceFormDetail = models.ForeignKey('UserInsuranceFormDetail', related_name='dataFieldValues')

    def __str__(self):
        return str(self.field) + " -> " + str(self.value)

    @property
    def value(self):
        if self.field.type == FieldType.TEXT:
            return self.char_val
        elif self.field.type == FieldType.DATE:
            return self.date_val
        elif self.field.type == FieldType.NUMBER:
            return self.number_val
        elif self.field.type == FieldType.ENUM:
            return self.enum_val
        else:
            raise ValueError("Coding error, invalid field type")

    @staticmethod
    def create(field, value, userInsuranceFormDetail):
        fieldData = DataFieldValue()
        fieldData.field = field
        fieldData.userInsuranceFormDetail = userInsuranceFormDetail

        if field.type == FieldType.TEXT:
            fieldData.char_val = value
        elif field.type == FieldType.DATE:
            fieldData.date_val = value
        elif field.type == FieldType.NUMBER:
            fieldData.number_val = value
        elif field.type == FieldType.ENUM:
            fieldData.enum_val = value
        else:
            raise ValueError("Coding error, invalid field type")

        fieldData.full_clean()
        fieldData.save()
        return fieldData

    def clean(self):
        DataFieldValue.validate(self.field, self.value)

    @staticmethod
    def validate(field, value):
        if value is None:
            raise ValidationError("Value not supplied")

        if field.type == FieldType.ENUM:
            if value not in field.enum_choices.all():
                raise ValidationError("Invalid enum choice selected")

        if field.type == FieldType.TEXT:
            if value == "":
                raise ValidationError("Empty string")

        if field.type == FieldType.NUMBER:
            if not isinstance(value, numbers.Number):
                raise ValidationError("Not type number")

        if field.type == FieldType.DATE:
            if not isinstance(value, datetime.date):
                raise ValidationError("Not type date")


class UserInsuranceFormDetail(models.Model):
    user = models.ForeignKey(get_user_model())
    insurance = models.ForeignKey(InsuranceForm)
