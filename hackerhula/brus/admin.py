from django.contrib import admin

from .models import *

admin.site.register(Machine)
admin.site.register(Product)
admin.site.register(Transaction)

