from django.conf.urls import include, url
from django.contrib import admin

import brus.views

urlpatterns = [
    url(r'^$', "brus.views.account", name="account"),
    url(r'^charge$', "brus.views.charge", name="charge"),
    url('sell', 'brus.views.sell')
]
