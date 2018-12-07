# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from core.models import EnumChoice, InsuranceForm, DataField


class EnumChoiceAdmin(ModelAdmin):
    class Meta:
        model = EnumChoice


class FieldAdmin(ModelAdmin):
    class Meta:
        model = DataField

class InsuranceFieldsAdmin(ModelAdmin):
    class Meta:
        model = InsuranceForm

admin.site.register(EnumChoice, EnumChoiceAdmin)
admin.site.register(DataField, FieldAdmin)
admin.site.register(InsuranceForm, InsuranceFieldsAdmin)