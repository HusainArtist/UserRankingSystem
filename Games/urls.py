# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


from .views import *
# from .swagger_schema import SwaggerSchemaView
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^search_by_prefix/', search_by_prefix, name='search_by_prefix'),
    # url(r'^swagger/', SwaggerSchemaView.as_view()),
    # url(r'^$', HomePageView.as_view(),name='home'),
    # url(r'^ajax_autocomplete/$', autocomplete, name='ajax_autocomplete'),
]
