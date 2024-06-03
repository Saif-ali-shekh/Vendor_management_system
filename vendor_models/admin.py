from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(VendorBaseUser)
admin.site.register(Vendor)
admin.site.register(Consumer)
admin.site.register(Product)
admin.site.register(PurchaseOrder)
admin.site.register(HistoricalPerformance)