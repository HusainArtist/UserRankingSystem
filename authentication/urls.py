from . import views
from django.conf.urls import include, url


urlpatterns = [
    url('', views.SignUp.as_view(), name='signup'),


]