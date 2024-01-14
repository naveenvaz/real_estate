from django.contrib import admin
from .models import *

admin.site.register(Property)
admin.site.register(Feature)
admin.site.register(Unit)
admin.site.register(Tenant)
admin.site.register(Agreement)
admin.site.register(Document)