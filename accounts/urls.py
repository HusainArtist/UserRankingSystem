# accounts/urls.py
from django.conf.urls import include, url

from . import views


urlpatterns = [
    url('signup/', views.SignUp.as_view(), name='signup'),
]