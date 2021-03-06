# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


from ecommapp.models import BaseCategory,SubCategory,Availibilty_status,Seller,Product,Pics,Customer,Cart,Cartitem,Delivery_Type,Order,Order_Status_Model,Payment_Method,Shipment_Orgs,Order_Product_Specs,Filter_Name,Filter_Category,Payment_Status,Flash_Sale,CustomerCouponUsed,CouponCode,Sales_Team,Tax,Brand,Phones,Size,CustomModulePics,TypeOfCustomProduct,Wish_List_Product,Wish_List,OrderReturn

from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.register(User,UserAdmin)
admin.site.register(CustomUser)
admin.site.register(BaseCategory)
admin.site.register(Wish_List_Product)
admin.site.register(Wish_List)
admin.site.register(SubCategory)
admin.site.register(Availibilty_status )
admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(Pics)
admin.site.register(Customer )
admin.site.register(Cart)
admin.site.register(Cartitem)
admin.site.register(Delivery_Type)
admin.site.register(Order)
admin.site.register(Order_Status_Model)
admin.site.register(Payment_Method)
admin.site.register(Shipment_Orgs)
admin.site.register(Payment_Status)
admin.site.register(Order_Product_Specs)
admin.site.register(Filter_Name)
admin.site.register(Filter_Category)
admin.site.register(Flash_Sale)
admin.site.register(CouponCode)
admin.site.register(CustomerCouponUsed)
admin.site.register(Sales_Team)
admin.site.register(Tax)
admin.site.register(Phones)
admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(CustomModulePics)
admin.site.register(TypeOfCustomProduct)
admin.site.register(OrderReturn)
