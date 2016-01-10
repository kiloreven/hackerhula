from django.contrib import admin

from .models import Member, PhysicalAccess, Membership

class MembershipInline(admin.TabularInline):
    model = Membership
    can_delete = False
    extra = 0

class MemberAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]

admin.site.register(Member, MemberAdmin)
admin.site.register(PhysicalAccess)
admin.site.register(Membership)

