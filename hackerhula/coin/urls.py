from django.conf.urls import include, url
from django.contrib import admin

import coin.views

app_name = "coin"
urlpatterns = [
    url(r'^$', "coin.views.account", name="coinaccount"),
    url(r'^charge$', "coin.views.charge"),
    url("sell", "coin.views.sell")
]
