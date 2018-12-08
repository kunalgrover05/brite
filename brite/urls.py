"""brite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework import permissions

import core.views
import userdata.views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Insurance API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^insuranceFields/(?P<pk>[0-9]+)/$', core.views.InsuranceFieldView.as_view()),
    url(r'^insuranceFields/$', core.views.InsuranceFieldsView.as_view()),
    url(r'^userData/$', userdata.views.UserDataView.as_view()),
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
