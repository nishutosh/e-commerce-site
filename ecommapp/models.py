# -*- coding: utf-8 -*-
#database for Fashvolts
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class BaseCategory(models.Model):
  Base_Category=models.CharField(max_length=100,unique=True)

class SubCategory(models.Model):
  Base_category=models.ForeignKey(BaseCategory)
  Sub_Category=models.CharField(max_length=100,unique=True)

class Availibilty_status(models.Model):
  status=models.CharField(max_length=50,unique=True)  

class Seller(models.Model):
  Seller_Id=models.CharField(max_length=100,unique=True)
  Seller_Name=models.CharField(max_length=100)
  Address=models.TextField(max_length=500)
  Profile=models.TextField(max_length=1000)
  email=models.EmailField()
  Contact_Number=models.IntegerField()
  Seller_Rating=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])

class Product_Status(models.Model):
   status=models.CharField(max_length=20,unique=True)
 


class Product(models.Model):
  Produce_Base_Category=models.ForeignKey(BaseCategory)
  product_Sub_Category=models.ForeignKey(SubCategory)
  Product_Name=models.CharField(max_length=200)
  Product_Code=models.TextField(max_length=100,unique=True)
  Price=models.FloatField()
  Availiability=models.ForeignKey(Product_Status)
  Description=models.TextField(max_length=10000)
  Features=models.TextField(max_length=10000)
  TechnicalSpecs=models.CharField(max_length=10000)
  color=models.CharField(max_length=50)
  discount=models.FloatField()
  

class Pics(models.Model):
  ProductPics=models.ForeignKey(Product)
  Images=models.ImageField(upload_to="ProductImages/")



class Customer(models.Model):
   User_customer=models.OneToOneField(User)
   Address_Line1=models.CharField(max_length=200)
   Address_Line2=models.CharField(max_length=200)
   City=models.CharField(max_length=200)
   State=models.CharField(max_length=200)
   ZIP=models.IntegerField()
   Volts_Credit=models.IntegerField(default=0)

class Customer_Card_Details(models.Model):
  Card_Customer=models.ForeignKey(Customer)
  Card_Number=models.IntegerField( validators=[MaxValueValidator(9999999999999999)])
  Owner=models.CharField(max_length=50)
  Date_Of_Expiry=models.DateField()
  CVV=models.IntegerField( validators=[MaxValueValidator(999)])

class Cart(models.Model):
   customer=models.ForeignKey(Customer)
   Cart_Id=models.CharField(max_length=100,unique=True)

class CartProduct(models.Model):
  Product_In_Cart=models.ForeignKey(Product)
  Cart_Product_Belongs_To=models.ForeignKey(Cart)




class Review(models.Model):
  Reviwer=models.ForeignKey(Customer)
  Product=models.ForeignKey(Product)
  Review_Title=models.CharField(max_length=200)
  Review_Body=models.TextField(max_length=5000)
  Product_Rating=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])



class Delivery_Type(models.Model):
   type=models.CharField(max_length=100,unique=True)

class Order(models.Model):
   Order_Id=models.CharField(max_length=200)
   Order_Customer=models.ForeignKey(Customer)
   Order_Delivery_Type=models.ForeignKey(Delivery_Type)
   Order_Date_Time=models.DateTimeField(auto_now_add=True)
   Order_Address_Line1=models.CharField(max_length=200)
   Order_Address_Line2=models.CharField(max_length=200)
   Order_City=models.CharField(max_length=200)
   Order_State=models.CharField(max_length=200)
   Order_ZIP=models.IntegerField()
   Order_Volts_Credit=models.IntegerField(default=0)
   Order_Contact_Number=models.IntegerField()

class Order_Status_Model(models.Model):
  status_for_order=models.CharField(max_length=100,unique=True)
  #delivered,shipped,outfordelivery,cancelled

class Payment_Method(models.Model):
   payment_type=models.CharField(max_length=100,unique=True)

class Shipment_Orgs(models.Model):
  Shipping_Company_Name=models.CharField(max_length=100)
  Shipping_Company_Id=models.CharField(max_length=100,unique=True)
  #shipping company details will be added as per requirements

class Payment_Status(models.Model):
  payment_status=models.CharField(max_length=100,unique=True)
  #pending,paid,cancelled



class Order_Product_Specs(models.Model):
  Order=models.ForeignKey(Order)
  Ordered_Product=models.ForeignKey(Product)
  Quantity=models.IntegerField(default=1)
  Order_Payment_Type=models.ForeignKey(Payment_Method)
  Order_Payment_status=models.ForeignKey(Payment_Status)
  Transaction_Id=models.CharField(max_length=100,unique=True)
  Invoice_Id=models.CharField(max_length=100,unique=True)
  Invoice=models.FileField(upload_to="Invoices/")
  Shipment_Authority=models.ForeignKey(Shipment_Orgs)
  Order_Status=models.ForeignKey(Order_Status_Model)
  Esimated_Dilivery_Date=models.DateField()

