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
# import Games.urls 
# import accounts.urls 
# from django.urls import path

# schema_view = get_swagger_view(title='Pastebin API')

# schema_view = get_schema_view(
#     title='Server Monitoring API',
#     url='https://www.example.org/api/',
#     renderer_classes=[JSONOpenAPIRenderer]
# )


urlpatterns = [
    # url('Games/', include('Games.urls')),
    url('admin/', admin.site.urls),
    # url('^schema.json$', schema_view),
    # url(r'docs/', schema_view),
	url(r'^docs/', SwaggerSchemaView.as_view()),
    url(r'^api/', include('Games.urls', namespace='games_urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api-auth/', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('accounts.urls'))
    # url(r'^docs/', include('rest_framework_swagger.urls', namespace='rest_framework'))
    # url(r'^docs/', include('rest_framework_swagger.urls')),
]