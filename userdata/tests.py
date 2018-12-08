# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase

# Only contains API Integration tests.
# Tests are not present for:
# 1- Unit tests for models: Most of it is covered through APIs
# 2- Admin: No custom forms, testing not needed
from rest_framework.test import APIClient

from core.models import DataField, FieldType, InsuranceForm, EnumChoice
from userdata.models import UserInsuranceFormDetail


class UserDataTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(first_name='Kunal')
        self.insuranceForm = InsuranceForm.objects.create(name='Health')
        self.locationField = DataField.objects.create(type=FieldType.TEXT, name='Location')
        self.ageField = DataField.objects.create(type=FieldType.NUMBER, name='Age')
        self.dobField = DataField.objects.create(type=FieldType.DATE, name='Date Of Birth')
        self.smokerField = DataField.objects.create(type=FieldType.ENUM, name='Smoker')
        self.smokerEnumChoice1 = EnumChoice.objects.create(name='Yes')
        self.smokerEnumChoice2 = EnumChoice.objects.create(name='No')
        self.smokerEnumChoiceInvalid = EnumChoice.objects.create(name='-1')
        self.smokerField.enum_choices.add(self.smokerEnumChoice1)
        self.smokerField.enum_choices.add(self.smokerEnumChoice2)

    def test_text_field(self):
        self.insuranceForm.fields.add(self.locationField)

        client = APIClient()
        resp = client.post('/userData/', {
            'insurance': self.insuranceForm.id,
            'user': self.user.pk,
            'dataFieldValues': [
                {
                    'fieldId': self.locationField.pk,
                    'value': 'Test123'
                }
            ]
        }, format='json')

        self.assertEqual(201, resp.status_code)

        # Verify created data
        createdUserInsuranceFormDetail = UserInsuranceFormDetail.objects.get(id=resp.data['id'])
        self.assertEqual(1, len(createdUserInsuranceFormDetail.dataFieldValues.all()))
        fieldValue = createdUserInsuranceFormDetail.dataFieldValues.all()[0]
        self.assertEqual('Test123', fieldValue.value)
        self.assertEqual(self.locationField, fieldValue.field)

    def test_numeric_field(self):
        self.insuranceForm.fields.add(self.ageField)

        client = APIClient()
        resp = client.post('/userData/', {
            'insurance': self.insuranceForm.id,
            'user': self.user.pk,
            'dataFieldValues': [
                {
                    'fieldId': self.ageField.pk,
                    'value': 123
                }
            ]
        }, format='json')

        self.assertEqual(201, resp.status_code)

        # Verify created data
        createdUserInsuranceFormDetail = UserInsuranceFormDetail.objects.get(id=resp.data['id'])
        self.assertEqual(1, len(createdUserInsuranceFormDetail.dataFieldValues.all()))
        fieldValue = createdUserInsuranceFormDetail.dataFieldValues.all()[0]
        self.assertEqual(123, fieldValue.value)
        self.assertEqual(self.ageField, fieldValue.field)

    def test_invalid_numeric_field(self):
        self.insuranceForm.fields.add(self.ageField)
        client = APIClient()
        resp = client.post('/userData/', {
            'insurance': self.insuranceForm.id,
            'user': self.user.pk,
            'dataFieldValues': [
                {
                    'fieldId': self.ageField.pk,
                    'value': 'Test'
                }
            ]
        }, format='json')

        self.assertEqual(400, resp.status_code)

    def test_date_field(self):
        self.insuranceForm.fields.add(self.dobField)

        client = APIClient()
        resp = client.post('/userData/', {
            'insurance': self.insuranceForm.id,
            'user': self.user.pk,
            'dataFieldValues': [
                {
                    'fieldId': self.dobField.pk,
                    'value': '2018-01-01'
                }
            ]
        }, format='json')
        self.assertEqual(201, resp.status_code)

        # Verify created data
        createdUserInsuranceFormDetail = UserInsuranceFormDetail.objects.get(id=resp.data['id'])
        self.assertEqual(1, len(createdUserInsuranceFormDetail.dataFieldValues.all()))
        fieldValue = createdUserInsuranceFormDetail.dataFieldValues.all()[0]
        self.assertEqual(datetime.datetime(2018, 01, 01).date(), fieldValue.value)
        self.assertEqual(self.dobField, fieldValue.field)

    def test_invalid_date_field(self):
        self.insuranceForm.fields.add(self.dobField)

        client = APIClient()
        resp = client.post('/userData/', {
            'insurance': self.insuranceForm.id,
            'user': self.user.pk,
            'dataFieldValues': [
                {
                    'fieldId': self.dobField.pk,
                    'value': 'Test'
                }
            ]
        }, format='json')

        self.assertEqual(400, resp.status_code)

    def test_enum_field(self):
        self.insuranceForm.fields.add(self.smokerField)

        client = APIClient()
        resp = client.post('/userData/', {
            'insurance': self.insuranceForm.id,
            'user': self.user.pk,
            'dataFieldValues': [
                {
                    'fieldId': self.smokerField.pk,
                    'value': self.smokerEnumChoice1.pk
                }
            ]
        }, format='json')

        self.assertEqual(201, resp.status_code)

        # Verify created data
        createdUserInsuranceFormDetail = UserInsuranceFormDetail.objects.get(id=resp.data['id'])
        self.assertEqual(1, len(createdUserInsuranceFormDetail.dataFieldValues.all()))
        fieldValue = createdUserInsuranceFormDetail.dataFieldValues.all()[0]
        self.assertEqual(self.smokerEnumChoice1, fieldValue.value)
        self.assertEqual(self.smokerField, fieldValue.field)

    def test_enum_field_invalid_data(self):
        self.insuranceForm.fields.add(self.smokerField)

        client = APIClient()
        resp = client.post('/userData/', {
            'insurance': self.insuranceForm.id,
            'user': self.user.pk,
            'dataFieldValues': [
                {
                    'fieldId': self.smokerField.pk,
                    'value': 'ABC'
                }
            ]
        }, format='json')

        self.assertEqual(400, resp.status_code)

    def test_enum_field_disallowed_choice(self):
        self.insuranceForm.fields.add(self.smokerField)

        client = APIClient()
        resp = client.post('/userData/', {
            'insurance': self.insuranceForm.id,
            'user': self.user.pk,
            'dataFieldValues': [
                {
                    'fieldId': self.smokerField.pk,
                    'value': self.smokerEnumChoiceInvalid.pk
                }
            ]
        }, format='json')

        self.assertEqual(400, resp.status_code)

    def test_create_data(self):
        self.insuranceForm.fields.add(self.locationField)
        self.insuranceForm.fields.add(self.ageField)
        self.insuranceForm.fields.add(self.dobField)
        self.insuranceForm.fields.add(self.smokerField)

        client = APIClient()
        resp = client.post('/userData/', {
            'insurance': self.insuranceForm.id,
            'user': self.user.pk,
            'dataFieldValues': [
                {
                    'fieldId': self.smokerField.pk,
                    'value': self.smokerEnumChoice1.pk
                },
                {
                    'fieldId': self.locationField.pk,
                    'value': 'India'
                },
                {
                    'fieldId': self.ageField.pk,
                    'value': 23
                }
                , {
                    'fieldId': self.dobField.pk,
                    'value': '1994-12-20'
                }
            ]
        }, format='json')

        self.assertEqual(201, resp.status_code)

        # Verify created data
        createdUserInsuranceFormDetail = UserInsuranceFormDetail.objects.get(id=resp.data['id'])
        self.assertEqual(4, len(createdUserInsuranceFormDetail.dataFieldValues.all()))

    def test_create_data_missing_field(self):
        self.insuranceForm.fields.add(self.locationField)
        self.insuranceForm.fields.add(self.ageField)
        self.insuranceForm.fields.add(self.dobField)
        self.insuranceForm.fields.add(self.smokerField)

        client = APIClient()
        resp = client.post('/userData/', {
            'insurance': self.insuranceForm.id,
            'user': self.user.pk,
            'dataFieldValues': [
                {
                    'fieldId': self.smokerField.pk,
                    'value': self.smokerEnumChoice1.pk
                },
                {
                    'fieldId': self.locationField.pk,
                    'value': 'India'
                },
                {
                    'fieldId': self.ageField.pk,
                    'value': 23
                }
            ]
        }, format='json')

        self.assertEqual(400, resp.status_code)

    def test_extra_field(self):
        self.insuranceForm.fields.add(self.locationField)

        client = APIClient()
        resp = client.post('/userData/', {
            'insurance': self.insuranceForm.id,
            'user': self.user.pk,
            'dataFieldValues': [
                {
                    'fieldId': self.smokerField.pk,
                    'value': self.smokerEnumChoice1.pk
                },
                {
                    'fieldId': self.locationField.pk,
                    'value': 'India'
                }
            ]
        }, format='json')

        self.assertEqual(400, resp.status_code)

    def test_retrieve_data(self):
        self.insuranceForm.fields.add(self.locationField)
        self.insuranceForm.fields.add(self.ageField)
        self.insuranceForm.fields.add(self.dobField)
        self.insuranceForm.fields.add(self.smokerField)

        client = APIClient()
        resp = client.post('/userData/', {
            'insurance': self.insuranceForm.id,
            'user': self.user.pk,
            'dataFieldValues': [
                {
                    'fieldId': self.smokerField.pk,
                    'value': self.smokerEnumChoice1.pk
                },
                {
                    'fieldId': self.locationField.pk,
                    'value': 'India'
                },
                {
                    'fieldId': self.ageField.pk,
                    'value': 23
                }
                , {
                    'fieldId': self.dobField.pk,
                    'value': '1994-12-20'
                }
            ]
        }, format='json')

        id = resp.data['id']
        # Verify created data
        resp = client.get('/userData/')

        self.assertEqual([{
            'id': id,
            'dataFieldValues': [{
                'field': 'Smoker',
                'value': 'Yes'
            }, {
                'field': 'Location',
                'value': 'India'
            }, {
                'field': 'Age',
                'value': '23'
            }, {
                'field': 'Date Of Birth',
                'value': '1994-12-20'
            }],
            'insuranceName': 'Health',
            'insurance': 1,
            'user': 1
        }], resp.data)
