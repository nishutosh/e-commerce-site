# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.views import View
from django.views.generic import DetailView,ListView
from .models import *
from django.http import Http404,JsonResponse
from django.views.generic.edit import FormView
from .forms import *
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.core.urlresolvers  import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

menu_product_view_context={
"base_category_list":BaseCategory.objects.all() 
}


class HomeView(ListView):
    model=BaseCategory
    context_object_name="base_category_list"
    template_name ="index.html"
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
             context["siteuser"]=self.request.user           
        return context

class ProductList(ListView):
  context_object_name="product_list"
  template_name="product_list.html"
  def get_queryset(self):
        try: 
              return  Product.objects.filter(Produce_Base_Category__Base_Slug_Field=self.kwargs["basefield"],product_Sub_Category__Sub_Category_Slug_Field=self.kwargs["subfield"])
        except:
              raise Http404
  def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context.update(menu_product_view_context)
        if self.request.user.is_authenticated:
             context["siteuser"]=self.request.user        
        return context
  
   


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
        context["pics"]=context["product"].pics_set.all()
        context.update(menu_product_view_context)
        if self.request.user.is_authenticated:
             context["siteuser"]=self.request.user      
        return context          
   
class RegisterView(FormView):
   template_name="register.html"
   form_class=RegisterForm
   success_url='/signin/'
   def form_valid(self, form):
        user_made=CustomUser.objects.create_user(username=form.cleaned_data["username"],password=form.cleaned_data["password"])
        Customer.objects.create(
                                       User_customer=user_made,
                                       Customer_First_Name=form.cleaned_data["first_name"],
                                       Customer_Last_Name=form.cleaned_data["last_name"],
                                       Customer_Email=form.cleaned_data["email"],
                                       Address_Line1=form.cleaned_data["address_line_1"],
                                       Address_Line2=form.cleaned_data["address_line_2"],
                                       City=form.cleaned_data["city"],
                                       State=form.cleaned_data["state"],
                                       ZIP=form.cleaned_data["ZIP"]  )
        messages.success(self.request, 'User Registered')
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
  def get_success_url(self):
             if "next" in self.request.GET.keys():
                 return  self.request.GET["next"]
             else:
                 return "/home/"   


class SignOutView(LoginRequiredMixin,View):
    def get(self,request):
          logout(request)
          return redirect(reverse("home"))


class PostGetCartView(View):

     CART_ID="CART_ID"
     def get(self,request): 
             cart=request.COOKIES.get(self.CART_ID)
             if cart:
                     new_cart_obj=Cart.objects.get(id=cart)
                     cart_items=new_cart_obj.cartitem_set.all()
                     cart_list=[]
                     for items in cart_items:
                         product_details={"Product_name":items.Product_In_Cart.Product_Name,
                                                         "Price":items.Total_Price(),
                                                         "Quantity":items.Product_Quantity}
                         cart_list.append(product_details)
                     return  JsonResponse(cart_list,safe=False)  
             else :
                     return  JsonResponse({"response":"no cokiee set"},safe=False)  

     def post(self,request):
             cart=request.COOKIES.get(self.CART_ID)
             if cart:
                 cart_obj=Cart.objects.get(pk=cart)
                 product=Product.objects.get(pk=request.POST["product"])
                 if cart_obj.cartitem_set.filter(Product_In_Cart=product).exists():

                       cart_obj.cartitem_set.filter(Product_In_Cart=product).update(Product_Quantity=request.POST["quantity"])
                 else:      
                       Cartitem.objects.create(Cart_Product_Belongs_To=cart_obj,Product_In_Cart=product,Product_Quantity=request.POST["quantity"])
                 response= JsonResponse({"response":"updated"},safe=False)  
             else:
                  new_cart_obj=Cart.objects.create(date_of_creation=timezone.now())
                  product=Product.objects.get(pk=request.POST["product"])
                  Cartitem.objects.create(Cart_Product_Belongs_To=new_cart_obj,Product_In_Cart=product,Product_Quantity=request.POST["quantity"])
                  response= JsonResponse({"response":"cookieson"},safe=False)   
                  response.set_cookie(self.CART_ID,new_cart_obj.pk)
             return response


class DeleteCartView(View):
     CART_ID="CART_ID"
     def  post(self,request):
               cart=request.COOKIES.get(self.CART_ID)
               if cart:
                     product=Product.objects.get(pk=request.POST["product"])
                     Cartitem.objects.filter(Product_In_Cart=product).delete()
               else:
                      return JsonResponse()
               return JsonResponse()

class CheckoutView(LoginRequiredMixin,View):
     CART_ID="CART_ID"
     def get(self,request):
            cart=request.COOKIES.get(self.CART_ID)
            if cart:
                 user=request.user
                 cart_obj=Cart.objects.get(pk=cart)
                 cart_items=cart_obj.cartitem_set.all()
                 context={"siteuser":user,"cart_items":cart_items}
                 print context
                 return render(request,"checkout.html",context)
            else:
                #disable checkout button
                return JsonResponse({"error":"nothing in cart"})
                  

















class OrderProducts(LoginRequiredMixin,View):

    pass
