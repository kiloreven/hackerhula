from django.contrib import admin

from .models import Member, PhysicalAccess
admin.site.register(Member)
admin.site.register(PhysicalAccess)
