# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import DataFieldValue, UserInsuranceFormDetail

class FieldDataAdmin(ModelAdmin):
    class Meta:
        model = DataFieldValue


class UserDataAdmin(ModelAdmin):
    class Meta:
        model = UserInsuranceFormDetail

admin.site.register(DataFieldValue, FieldDataAdmin)
admin.site.register(UserInsuranceFormDetail, UserDataAdmin)