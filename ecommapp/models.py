# -*- coding: utf-8 -*-
#database for Fashvolts
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Alll the users use this model to store their details
    username(//unique)
    profile Pic
    UUID(//automatically generated // auto increment// unique)
    password(AbstactBaseClass)
    """
    username=models.CharField(max_length=50,unique=True)
    is_active=models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def get_full_name(self):
          return self.username

    def get_short_name(self):
          return self.username

    USERNAME_FIELD='username'
    REQUIRED_FIELD=['']

    objects=CustomUserManager()
    def __str__(self):
        return self.username



class BaseCategory(models.Model):
  Base_Category=models.CharField(max_length=100,unique=True)
  Base_Category_Pic=models.ImageField(upload_to="BaseCatPic/")
  Base_Slug_Field=models.SlugField(max_length=120,blank=True)
  def save(self, *args, **kwargs):
        print (self.Base_Category)
        self.Base_Slug_Field=slugify(self.Base_Category)
        super(BaseCategory, self).save()
  def __str__(self):
     return self.Base_Category



class SubCategory(models.Model):
  Base_category_Key=models.ForeignKey(BaseCategory)
  Sub_Category=models.CharField(max_length=100)
  Sub_Category_alias = models.CharField(max_length = 20, default = "sub")
  Sub_Category_Pic=models.ImageField(upload_to="SubCatPic/")
  Sub_Category_Slug_Field=models.SlugField(max_length=120,blank=True)
  def save(self, *args, **kwargs):
        self.Sub_Category_Slug_Field=slugify(self.Sub_Category)
        super(SubCategory, self).save()
  def __str__(self):
    return self.Sub_Category

class Tax(models.Model):
    Products=models.ForeignKey(SubCategory)
    Tax_Percentage=models.FloatField()
    

class Filter_Name(models.Model):
   Filter_Name=models.CharField(max_length=100)
   Filter_Subcategory_Type=models.ForeignKey(SubCategory)
   def __str__(self):
        return self.Filter_Name

class Filter_Category(models.Model):
   Filter=models.ForeignKey(Filter_Name)
   Filter_Category_Name=models.CharField(max_length=100)
   def __str__(self):
        return self.Filter_Category_Name

class Availibilty_status(models.Model):
  status=models.CharField(max_length=50,unique=True)
  def __str__(self):
        return self.status

class Seller(models.Model):
  seller_user=models.OneToOneField(CustomUser)
  Seller_Id=models.CharField(max_length=100,unique=True)
  Seller_Name=models.CharField(max_length=100)
  Address=models.TextField(max_length=500)
  Profile=models.TextField(max_length=1000)
  email=models.EmailField()
  Contact_Number=models.IntegerField()
  def __str__(self):
        return self.Seller_Id

class Shipment_Orgs(models.Model):
  Shipping_Company_Name=models.CharField(max_length=100)
  Shipping_Company_URL=models.URLField(max_length=100)
  def __str__(self):
        return self.Shipping_Company_Name
  #shipping company details will be added as per requirements
class Size(models.Model):
  size_sf=models.CharField(max_length=20)



class Product(models.Model):
  Product_Base_Category=models.ForeignKey(BaseCategory)
  product_Sub_Category=models.ForeignKey(SubCategory)
  Product_Name=models.CharField(max_length=200)
  Discount=models.FloatField(default=0)
  Base_Price=models.FloatField()
  Availiability=models.BooleanField(default=True)
  Description=models.TextField(max_length=10000,blank=True)
  Features=models.TextField(max_length=10000,blank=True)
  TechnicalSpecs=models.CharField(max_length=10000,blank=True)
  # Product_Filter=models.ManyToManyField(Filter_Category)
  Main_Image=models.ImageField(upload_to="ProductImages/")
  Shipment_Authority=models.ForeignKey(Shipment_Orgs)
  is_displayed=models.BooleanField(default=True)
  Product_Seller=models.ForeignKey(Seller)
  TaxOnProduct=models.ForeignKey(Tax)
  Sizes=models.ManyToManyField(Size)
  def __str__(self):
     return str(self.Product_Name)
  
  def get_product_url(self):
      return "product/"+str(self.Product_Base_Category.Base_Slug_Field)+"/"+str(self.product_Sub_Category.Sub_Category_Slug_Field)+"/"+str(self.pk)
  def price_after_discount(self):
      Actual_Price=((100-self.Discount)/100)* self.Base_Price
      price_after_tax=Actual_Price+((self.TaxOnProduct.Tax_Percentage/100)*Actual_Price)
      return  price_after_tax
  def indexing(self):
     from .search import ProductIndex
     obj = ProductIndex(
        meta={'id': self.id},
        Product_Name=self.Product_Name,
        Description=self.Description,
        Features=self.Features,
        TechnicalSpecs=self.TechnicalSpecs
     )
     obj.save()
     return obj.to_dict(include_meta=True)

class Flash_Sale(models.Model):
   Flash_Sale_Name=models.CharField(max_length=100)
   Products_In_Sale=models.ManyToManyField(Product)
   active=models.BooleanField(default=False)
   Main_Banner=models.ImageField(upload_to="FlashSaleBanner/")
   Flash_Sale_URL=models.URLField()
   def __str__(self):
     return self.Flash_Sale_Name




class Pics(models.Model):
  ProductPics=models.ForeignKey(Product)
  Images=models.ImageField(upload_to="ProductImages/")
  def __str__(self):
     return self.Images.name


class Customer(models.Model):
   User_customer=models.OneToOneField(CustomUser)
   Customer_First_Name=models.CharField(max_length=100)
   Customer_Last_Name=models.CharField(max_length=100)
   Customer_Email=models.CharField(max_length=100)
   Address_Line1=models.CharField(max_length=200)
   Address_Line2=models.CharField(max_length=200)
   City=models.CharField(max_length=200)
   State=models.CharField(max_length=200)
   ZIP=models.IntegerField()
   Customer_Contact_Number=models.IntegerField()
   Volts_Credit=models.IntegerField(default=0)
   User_Profile_Pic=models.ImageField(upload_to="UserProfilePic/",null=True)
   usability=models.BooleanField(default=True)
   can_create_custom=models.BooleanField(default=True)
   Join_Date_Time = models.DateTimeField(auto_now_add = True,blank = True)
   def __str__(self):
     return self.Customer_First_Name

# class Review(models.Model):
#   Reviewer=models.ForeignKey(Customer)
#   Product=models.ForeignKey(Product)
#   Review_Title=models.CharField(max_length=200)
#   Review_Body=models.TextField(max_length=5000)
#   show_review=models.BooleanField(default=True)

class Wish_List(models.Model):
   User_Wishlist=models.OneToOneField(CustomUser)


class Wish_List_Product(models.Model):
   Product_In_Wishlist=models.ForeignKey(Product)
   Wishlist=models.ForeignKey(Wish_List)


class Sales_Team(models.Model):
   Sales_user=models.OneToOneField(CustomUser)
   Sales_First_Name=models.CharField(max_length=100)
   Sales_Last_Name=models.CharField(max_length=100)
   Sales_Email=models.CharField(max_length=100)
   is_intern=models.BooleanField(default=False)
   Sales_Contact_Number=models.IntegerField()
   Sales_Points=models.IntegerField(default=0)
   def __str__(self):
     return self.Sales_First_Name

#coupon stuff
class CouponCode(models.Model):
    Code=models.CharField(max_length=100)
    Sales_Member=models.ForeignKey(Sales_Team,null=True,blank=True)
    Discount=models.FloatField(default=0)
    def __str__(self):
       return self.Code




class CustomerCouponUsed(models.Model):
    customer_track=models.ForeignKey(Customer)
    coupon_code=models.ForeignKey(CouponCode)

#cart stuff
class Cart(models.Model):
   date_of_creation=models.DateField(auto_now_add=True)
   checkout_date=models.DateField(blank=True,null=True)
   coupon_code=models.ForeignKey(CouponCode,null=True,blank=True)
   credits_used=models.IntegerField(default=0)
   def Total_cart_Price(self):
        total_cart_price=0
        for products in self.cartitem_set.all():
          total_cart_price+=products.Total_Price() 
        return total_cart_price
   def final_cart_price(self):
       bill=self.Total_cart_Price()
       if self.coupon_code:
          bill=bill-self.coupon_code.Discount
       if self.credits_used:
          bill=bill-self.credits_used
       return bill   
   def OrderReferenceCheck(self):
        if self.coupon_code:
             return self.coupon_code.Sales_Member
        else:
             return None

class Cartitem(models.Model):
  Cart_Product_Belongs_To=models.ForeignKey(Cart)
  Product_In_Cart=models.ForeignKey(Product)
  Product_Quantity=models.IntegerField(default=1)
  def Total_Price(self):
          Total=(self.Product_In_Cart.price_after_discount())*(self.Product_Quantity)
          return Total
  def ProductAvailibiltyCheck(self):
         if self.Product_In_Cart.Availiability:
             return self.Product_In_Cart
         else:
             return None
  # def CalculateEstimateDate(self):
  #       return timezone.now()


#order stuff

class Delivery_Type(models.Model):
   type=models.CharField(max_length=100,unique=True)
   def __str__(self):
       return self.type
   #normal #express

class Payment_Method(models.Model):
  payment_type=models.CharField(max_length=100,unique=True)
  def __str__(self):
       return self.payment_type

class Payment_Status(models.Model):
  payment_status=models.CharField(max_length=100,unique=True)
  def __str__(self):
       return self.payment_status

class Order_Status_Model(models.Model):
  status_for_order=models.CharField(max_length=100,unique=True)
  def __str__(self):
       return self.status_for_order
  #delivered,shipped,outfordelivery,cancelled
class Order(models.Model):
   Order_In_Name_Of=models.CharField(max_length=100)
   Order_Customer=models.ForeignKey(Customer)
   Order_Delivery_Type=models.ForeignKey(Delivery_Type)
   Order_Date_Time=models.DateTimeField(auto_now_add=True)
   Order_Payment_Date=models.DateTimeField(null=True,blank=True)
   Order_Address_Line1=models.CharField(max_length=200)
   Order_Address_Line2=models.CharField(max_length=200)
   Order_City=models.CharField(max_length=200)
   Order_State=models.CharField(max_length=200)
   Order_ZIP=models.IntegerField()
   Invoice_visible=models.BooleanField(default=False)
   Order_Payment_Type=models.ForeignKey(Payment_Method)
   Order_Payment_status=models.ForeignKey(Payment_Status)
   Transaction_Id=models.CharField(max_length=100,blank=True)
   coupon_code_used_in_order=models.ForeignKey(CouponCode,null=True,blank=True)
   credits_used_in_order=models.IntegerField(default=0)
   Order_Price_Raw=models.IntegerField()
   Order_Total_Price=models.IntegerField()
   Order_Reference=models.ForeignKey(Sales_Team,null=True,blank=True)
   class Meta:
       ordering=['-Order_Date_Time']
   def __str__(self):
       return self.Order_In_Name_Of


def OrderPaymentOptionCheck(method_request):
          if Payment_Method.objects.filter(payment_type=method_request).exists():
                return  Payment_Method.objects.get(payment_type=method_request)
          else:
                return None



class Order_Product_Specs(models.Model):
  Order=models.ForeignKey(Order)
  Ordered_Product=models.ForeignKey(Product)
  Quantity=models.IntegerField(default=1)
  #Invoice_Id=models.CharField(max_length=100,unique=True)
  #Invoice=models.FileField(upload_to="Invoices/")
  Shipment_Authority_Details=models.ForeignKey(Shipment_Orgs)
  Shipment_Id=models.CharField(max_length=100)
  #Esimated_Delivery_Date=models.DateField()
  Order_Status=models.ForeignKey(Order_Status_Model)
  Final_Ordered_Product_price=models.FloatField()
  Order_Volts_Credit_Used=models.IntegerField(default=0)

class OrderReturn(models.Model):
   Product=models.ForeignKey(Order_Product_Specs)
   Reason = models.CharField(max_length = 100)
   def __str__(self):
        return self.Product.Ordered_Product.Product_Name
   
class TypeOfCustomProduct(models.Model):
    product_type = models.CharField(max_length = 20,unique=True)
    image = models.ImageField(upload_to = "CustomTypes/")
    sub_category = models.ForeignKey(SubCategory)
    def __str__(self):
        return self.product_type   


class Brand(models.Model):
  brand_name=models.CharField(max_length=100,unique=True)
  brand_type = models.ForeignKey(TypeOfCustomProduct,default = 1) 
  brand_pic=models.ImageField(upload_to="BrandPic/")
  slug=models.CharField(max_length=100,blank=True)
  def save(self, *args, **kwargs):
        self.slug=slugify(self.brand_name)
        super(Brand, self).save()
  def __str__(self):
    return self.brand_name      

class Phones(models.Model):
  brand=models.ForeignKey(Brand)
  name=models.CharField(max_length=100)
  pic=models.ImageField(upload_to="CustomImages/")
  def __str__(self):
      return self.brand.brand_name+self.name

class CustomModulePics(models.Model):
    main_image = models.ImageField(upload_to="CustomWorkImages/")
    preview = models.ImageField(upload_to="CustomWorkImages/")
    text_to_be_inserted = models.CharField(max_length=20,blank=True,null=True)
    product = models.ForeignKey(Product)    
    def __str__(self):
        return self.product.Product_Name
   
 
