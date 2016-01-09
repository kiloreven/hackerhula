"""hackerhula URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

from django.conf import settings
from django.conf.urls.static import static

from member import urls as member_urls
from spaceapi import urls as spaceapi_urls
from coin import urls as coin_urls

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/hula/', permanent=False)),
    url(r'^hula/$', TemplateView.as_view(template_name="frontpage.html")),
    url(r'^hula/member/', include(member_urls)),
    url(r'^hula/spaceapi/', include(spaceapi_urls)),
    url(r'^hula/admin/', include(admin.site.urls)),
    url(r'^hula/coin/', include(coin_urls)),
]

# Serve the static files ourselves.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
