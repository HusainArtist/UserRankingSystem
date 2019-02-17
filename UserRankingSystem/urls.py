"""UserRankingSystem URL Configuration

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
from django.conf import settings
# from rest_framework_swagger.views import get_swagger_view

# from rest_framework.documentation import include_docs_urls

# from django.contrib import admin

# from rest_framework.schemas import get_schema_view
# from rest_framework.renderers import JSONOpenAPIRenderer

import rest_framework

from django.contrib import admin
from django.conf.urls import include, url
from UserRankingSystem.swagger_schema import SwaggerSchemaView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('admin/', admin.site.urls),

	url(r'^docs/', SwaggerSchemaView.as_view()),
    url(r'^api/', include('Games.urls', namespace='games_urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^signup/', include('authentication.urls')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

   
]