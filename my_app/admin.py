from django.contrib import admin
from .models import * 
import re

# Register your models here.
admin.site.site_header = "Al-Ard Library Admin"
admin.site.register( Employee )
admin.site.register( Manager )
admin.site.register( Product )
admin.site.register( ProductAttribute )
admin.site.register( Purchase )
admin.site.register( Purchase_item )
admin.site.register( Sale_order )
admin.site.register( Sale_item )
admin.site.register( Supplier )
admin.site.register( Customer )
admin.site.register( Currency )
admin.site.register( ExchangeRate )
admin.site.register( CompanyProfile )
admin.site.register( Stock_Out_Voucher )
admin.site.register( Stock_Out_Voucher_item )
admin.site.register( SaleReturn )

# admin.site.register( Category )
