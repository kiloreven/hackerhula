from django.conf.urls import include, url
from django.contrib import admin

import spaceapi.views

urlpatterns = [
    url(r'^spaceapi.json$', "spaceapi.views.spaceapi", name="spaceapi_endpoint"),
]
