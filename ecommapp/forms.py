from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator,MinimumLengthValidator,CommonPasswordValidator,NumericPasswordValidator
from .models import CustomUser,Customer




class RegisterForm(forms.Form):
    username=forms.CharField(max_length=50,min_length=8)
    password=forms.CharField(widget=forms.PasswordInput,validators=[],help_text='Your password  should have blah blah blah..')
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    first_name=forms.CharField(max_length=50)
    last_name=forms.CharField(max_length=50)
    email=forms.EmailField()
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




    
