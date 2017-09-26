from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator,MinimumLengthValidator,CommonPasswordValidator,NumericPasswordValidator
from .models import CustomUser,Customer,Payment_Method,Delivery_Type




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
    city=forms.CharField(max_length=200)  
    state=forms.CharField(max_length=200)
    ZIP=forms.IntegerField()

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password= cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
                raise forms.ValidationError(
                    "Password and confirm Password fields does not match"
                )
                
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



Delivery_City=[
    "Qila Rai Pithora",
    "Siri",
    "Tughlqabad",
    "Jahanpanah",
    "Firozobad",
    "Mehrauli",
    "Shahjahanabad",
    "New Delhi"
]

Delivery_Modes=[]
delivery_modes=Delivery_Type.objects.all()
for delivery_types in delivery_modes:
  Delivery_Modes.append(delivery_types.type)

Payment_Type=[]
payment_methods=Payment_Method.objects.all()
for methods in payment_methods:
    Payment_Method.append(methods.payment_type)


class PlaceOrderForm(forms.Form):
     """
     fields to be added in front end
     payment option select button
     terms and condition checkbox
     """
     #billing details
     Your_Name=forms.CharField(max_length=200)
     Order_In_Name_Of=forms.CharField(max_length=100)
     Order_Address_Line1=forms.CharField(max_length=200)
     Order_Address_Line2=forms.CharField(max_length=200)
     Order_City=forms.ChoiceField(widget=forms.Select,choices=Delivery_City)
     #default state delhi
     Order_ZIP=forms.CharField(max_length=20)
     Same_As_Shipping_Address=forms.ChoiceField(widget=forms.CheckboxInput)
     #delievry type
     Delivery_Type=forms.ChoiceField(widget=forms.RadioSelect,choices=Delivery_Modes)
     #payment option
     Payment_Method=forms.ChoiceField(widget=forms.RadioSelect,choices=Payment_Type)
     Terms_and_Condition=forms.ChoiceField(widget=forms.CheckboxInput)

     
     

   
