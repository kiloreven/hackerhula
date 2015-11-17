from django.conf.urls import include, url
from django.contrib import admin

import member.views

urlpatterns = [
    url(r'^$', "member.views.memberlist", name="memberlist"),
    url(r'^dooraccess$', "member.views.dooraccess", name="dooraccess"),
    url(r'^unixaccount$', "member.views.unixaccount", name="unixaccount"),
]
