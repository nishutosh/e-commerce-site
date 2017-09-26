# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


from ecommapp.models import BaseCategory,SubCategory,Availibilty_status,Seller,Product,Pics,Customer,Cart,Cartitem,Review,Delivery_Type,Order,Order_Status_Model,Payment_Method,Shipment_Orgs,Order_Product_Specs,Filter_Name,Filter_Category,Payment_Status
from .models import CustomUser

admin.site.register(CustomUser)
admin.site.register(BaseCategory)
admin.site.register(SubCategory)
admin.site.register(Availibilty_status )
admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(Pics)
admin.site.register(Customer )
admin.site.register(Cart)
admin.site.register(Cartitem)
admin.site.register(Review)
admin.site.register(Delivery_Type)
admin.site.register(Order)
admin.site.register(Order_Status_Model)
admin.site.register(Payment_Method)
admin.site.register(Shipment_Orgs)
admin.site.register(Payment_Status)
admin.site.register(Order_Product_Specs)
admin.site.register(Filter_Name)
admin.site.register(Filter_Category)
