from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator,MinimumLengthValidator,CommonPasswordValidator,NumericPasswordValidator
from .models import CustomUser,Customer,Payment_Method,Delivery_Type
from django.forms import ModelForm
from .models import *




# class RegisterForm(forms.Form):
#     username=forms.CharField(max_length=50,min_length=8)
#     password=forms.CharField(widget=forms.PasswordInput,validators=[],help_text='Your password  should have blah blah blah..')
#     confirm_password=forms.CharField(widget=forms.PasswordInput)
#     first_name=forms.CharField(max_length=50)
#     last_name=forms.CharField(max_length=50)
#     email=forms.EmailField()
#     contact_number=forms.IntegerField()
#     address_line_1=forms.CharField(max_length=400)
#     address_line_2=forms.CharField(max_length=400)
#     city=forms.CharField(max_length=200)
#     state=forms.CharField(max_length=200)
#     ZIP=forms.IntegerField()
#
#     def clean(self):
#         cleaned_data = super(RegisterForm, self).clean()
#         password= cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")
#         if password != confirm_password:
#                 raise forms.ValidationError(
#                     "Password and confirm Password fields does not match"
#                 )

class SignInForm(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField(widget=forms.PasswordInput)


class AccountEditForm(forms.Form):
    email=forms.EmailField()
    contact_number=forms.IntegerField()
    address_line_1=forms.CharField(max_length=400)
    address_line_2=forms.CharField(max_length=400)
    city=forms.CharField(max_length=200)
    state=forms.CharField(max_length=200)
    ZIP=forms.IntegerField()

class PasswordChange(forms.Form):
    old_password=forms.CharField(widget=forms.PasswordInput)
    password=forms.CharField(widget=forms.PasswordInput,validators=[],help_text='Your password  should have blah blah blah..')
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super(PasswordChange, self).clean()
        password= cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
                raise forms.ValidationError("Password and confirm Password fields does not match" )



Delivery_City=(
    ("1","Qila Rai Pithora"),
    ("2","Siri"),
    ("3","Tughlqabad"),
)

Delivery_Modes=(("EXPRESS","EXPRESS"),
                                  ("NORMAL","NORMAL"),)
# delivery_modes=Delivery_Type.objects.all()
# for delivery_types in delivery_modes:
#   Delivery_Modes.append(delivery_types.type)

Payment_Type=(("CASH ON DELIVERY","CASH ON DELIVERY"),
                                  ("ONLINE BANKING","ONLINE BANKING"),)
# payment_methods=Payment_Method.objects.all()
# for methods in payment_methods:
#     Payment_Method.append(methods.payment_type)


class PlaceOrderForm(forms.Form):
     """
     fields to be added in front end
     payment option select button
     terms and condition checkbox
     """
     #billing details
     Order_In_Name_Of=forms.CharField(max_length=100)
     Order_Address_Line1=forms.CharField(max_length=200)
     Order_Address_Line2=forms.CharField(max_length=200)
     Order_Region=forms.ChoiceField(widget=forms.Select,choices=Delivery_City)
     #default state delhi
     Order_ZIP=forms.IntegerField()
     #Same_As_Shipping_Address=forms.ChoiceField(widget=forms.CheckboxInput)
     #delievry type
     Delivery_Type=forms.ChoiceField(widget=forms.RadioSelect,choices=Delivery_Modes)
     #payment option
     Payment_Method=forms.ChoiceField(widget=forms.RadioSelect,choices=Payment_Type)
     Terms_and_Condition=forms.BooleanField(required=True)

     def clean_terms_and_condition(self):
          if self.cleaned_data["Terms_and_Condition"]:
              return self.cleaned_data["Terms_and_Condition"]
          else:
              raise ValidationError("you must accept the terms and condition")



class RegisterForm(forms.Form):
    username=forms.CharField(max_length=50,min_length=8)
    password=forms.CharField(widget=forms.PasswordInput,validators=[],help_text='Your password  should have blah blah blah..')
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    first_name=forms.CharField(max_length=50)
    last_name=forms.CharField(max_length=50)
    email=forms.EmailField()
    contact_number=forms.IntegerField()
    address_line_1=forms.CharField(max_length=400)
    address_line_2=forms.CharField(max_length=400)
    Region=forms.ChoiceField(widget=forms.Select,choices=Delivery_City)
    #state=forms.CharField(max_length=200)
    ZIP=forms.IntegerField()
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password= cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
                raise forms.ValidationError(
                    "Password and confirm Password fields does not match"
                )
class BaseCategoryForm(ModelForm):
      class Meta:
          model = BaseCategory
          fields=["Base_Category","Base_Category_Pic"]

class SubCategoryForm(ModelForm):
      class Meta:
           model=SubCategory
           fields=["Base_category_Key","Sub_Category","Sub_Category_Pic"]
           
