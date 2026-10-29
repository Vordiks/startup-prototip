from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(COMPANY)
admin.site.register(purchase)
admin.site.register(Product)
admin.site.register(Warehouse)
admin.site.register(Stock)
