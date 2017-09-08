# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.views import View
from django.views.generic import DetailView,ListView
from .models import BaseCategory,Product
from django.http import Http404
from django.views.generic.edit import FormView
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.urlresolvers  import reverse
from django.shortcuts import redirect

class HomeView(ListView):
    model=BaseCategory
    context_object_name="base_category_list"
    template_name ="index.html"

class ProductList(ListView):
  context_object_name="product_list"
  template_name="product_list.html"
  def get_queryset(self):
        try: 
              return  Product.objects.filter(Produce_Base_Category__Base_Slug_Field=self.kwargs["basefield"],product_Sub_Category__Sub_Category_Slug_Field=self.kwargs["subfield"])
        except:
              raise Http404
  
   


class ProductDetails(DetailView):
   context_object_name="product"
   template_name="product.html"
   def get_queryset(self):
        try:
            return  Product.objects.filter(Produce_Base_Category__Base_Slug_Field=self.kwargs["basefield"],product_Sub_Category__Sub_Category_Slug_Field=self.kwargs["subfield"],pk=self.kwargs["pk"])
        except:
              raise Http404 

   def get_context_data(self, **kwargs):
        context = super(ProductDetails, self).get_context_data(**kwargs)
        context["pics"]=context["product"].pics_set.filter(Is_Detail_Image=True)
        print context
        return context          
   
class RegisterView(FormView):
   template_name="register.html"
   form_class=RegisterForm
   success_url='/account-created/'
   def form_valid(self, form):
        form.create_user()
        return super(RegisterView, self).form_valid(form)
   

class SignInView(FormView):
  """
  Login class
  """
  template_name="signin.html"
  form_class=SignInForm
  success_url="/home/"
  def form_valid(self,form):
        user=authenticate(self.request,username=form.cleaned_data["username"],password=form.cleaned_data["password"])
        if user is not None:
             login(self.request,user)
        else:
             messages.error(self.request, 'Invalid username or password')
             return redirect(reverse("signin"))
        return super(SignInView, self).form_valid(form)


    


# Create your views here.
