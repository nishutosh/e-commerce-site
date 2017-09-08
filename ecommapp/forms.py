from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import CustomUser,Customer




class RegisterForm(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField(widget=forms.PasswordInput,validators=[RegexValidator()],help_text='Your password  should have blah blah blah..')
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
    def create_user(self):
        user_made=CustomUser.objects.create_user(username=self.cleaned_data["username"],password=self.cleaned_data["password"])
        Customer.objects.create(
                                       User_customer=user_made,
                                       Customer_First_Name=self.cleaned_data["first_name"],
                                       Customer_Last_Name=self.cleaned_data["last_name"],
                                       Customer_Email=self.cleaned_data["email"],
                                       Address_Line1=self.cleaned_data["address_line_1"],
                                       Address_Line2=self.cleaned_data["address_line_2"],
                                       City=self.cleaned_data["city"],
                                       State=self.cleaned_data["state"],
                                       ZIP=self.cleaned_data["ZIP"]  )



    
