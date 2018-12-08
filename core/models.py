# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class FieldType(object):
    TEXT = 'text'
    NUMBER = 'number'
    DATE = 'date'
    ENUM = 'enum'


class EnumChoice(models.Model):
    """
    Choices for Enum fields. Should be selected at time of creation of Enum field.
    """
    name = models.CharField(max_length=190)

    def __str__(self):
        return self.name


class DataField(models.Model):
    """
    A Data field representation. Each field has a field name and type.
    Enum fields should have enum_choices that are allowed for this field.
    """
    # TODO: We can't confirm that enum choices are necessarily present for Enum fields here, because
    # save happens before M2M relations are done. All validation should be part of API / Forms.

    name = models.CharField(max_length=190)
    type = models.CharField(max_length=10, choices=[(FieldType.TEXT, 'Text field'), (FieldType.NUMBER, 'Number Field'),
                                                    (FieldType.DATE, 'Date Field'), (FieldType.ENUM, 'Enum Field')])
    enum_choices = models.ManyToManyField(EnumChoice, blank=True)

    def __str__(self):
        return self.name


class InsuranceForm(models.Model):
    """
    A model representing an Insurance Form. Each form has a name and a set of DataFields associated
    with that form.
    """
    name = models.CharField(max_length=190)
    fields = models.ManyToManyField(DataField)

    def __str__(self):
        return self.name