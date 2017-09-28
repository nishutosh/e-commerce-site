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
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.utils import timezone
from django.contrib.auth.decorators import login_required


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
class UserNameCheckView(View):
    """checks username exist or not during registartion process"""
    def get(self,request):
           if "username" in request.GET:
                if CustomUser.objects.filter(username=request.GET["username"]).exist():
                    return JsonResponse({"message":"username already exist"})
                else:
                     return JsonResponse({"message":"Good to go"})  
           else:
                 return JsonResponse({"message":"error no username field"})  


class RegisterView(FormView):
   template_name="register.html"
   form_class=RegisterForm
   success_url='auth/signin/'
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
                                       ZIP=form.cleaned_data["ZIP"],
                                       Customer_Contact_Number=form.cleaned_data["contact_number"] )
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
            if user.is_active:
                  login(self.request,user)
                  return super(SignInView, self).form_valid(form)
            else:
                 messages.error(self.request, 'Invalid username or password')
                 return redirect(reverse("signin"))    
        else:
             messages.error(self.request, 'Invalid username or password')
             return redirect(reverse("signin"))
  def get_success_url(self):
             if "next" in self.request.GET.keys():
                 return  self.request.GET["next"]
             else:
                 return "/home/"   


class SignOutView(LoginRequiredMixin,View):
    def get(self,request):
          logout(request)
          return redirect(reverse("home"))


# class ReviewFormView(LoginRequiredMixin,FormView):
#     """user submit review"""
#     template_name="user-review"
#     form_class=ReviewForm
#     def form_valid(self,form):
#         Review.objects.create(Reviewer=self.request.user,
#                                                Product=self.kwargs["product"],
#                                                Review_Title=form.cleaned_data["Review_titile"],
#                                                Review_Body=form.cleaned_data["Review_Body"],
#                                                show_review=True)
#         messages.success(self.request, 'Review Submitted')
#         return super(RegisterView, self).form_valid(form)


class UserDashboard(LoginRequiredMixin,View):
    """user home page"""
    template_name="userhome.html"
    context_object_name = "siteuser"
    def get(self,request):
           context={"siteuser":request.user}
           context.update(menu_product_view_context)
           return render(request,self.template_name,context) 

class  EditFormView(LoginRequiredMixin,FormView):
    """user edit details"""
    success_url="user/user-dashboard/"
    template_name="user-edit-form.html"
    form_class=AccountEditForm
    def get_initial(self):
          user_obj=self.request.user
          initial={
                      "email":user_obj.customer.Customer_Email,
                      "contact_number":user_obj.customer.Customer_Contact_Number,
                      "address_line_1":user_obj.customer.Address_Line1,
                      "address_line_2":user_obj.customer.Address_Line2,
                      "city":user_obj.customer.City,
                      "state":user_obj.customer.State,
                      "ZIP":user_obj.customer.ZIP,
                      }
          return initial

    def form_valid(self,form):
          user_obj=self.request.user
          Customer.objects.filter(User_customer=user_obj).update(
                                                        Customer_Email=form.cleaned_data["email"],
                                                        Address_Line1=form.cleaned_data["address_line_1"],
                                                        Address_Line2=form.cleaned_data["address_line_2"],
                                                        City=form.cleaned_data["city"],
                                                        State=form.cleaned_data["state"],
                                                        ZIP=form.cleaned_data["ZIP"],
                                                        Customer_Contact_Number=form.cleaned_data["contact_number"] )
          messages.success(self.request, 'Details Updated')
          return super(EditFormView, self).form_valid(form)

class SecurityView(LoginRequiredMixin,FormView):
    success_url="user/user-dashboard/"
    template_name="security.html"
    form_class=PasswordChange
    def form_valid(self,form):
          user_obj=self.request.user
          if not user_obj.check_password(form.cleaned_data["old_password"]):
                raise forms.ValidationError("Old password does not match")
          else:
                user_obj.set_password(form.cleaned_data["password"]) 
                user_obj.save()  
                messages.success(self.request, 'Password Changed')
                return super(SecurityView, self).form_valid(form)



class FashVoltsCreditView(LoginRequiredMixin,View):
     def get(self,request):
         user_obj=request.user
         context={"siteuser":user_obj,"credits":user_obj.customer.Volts_Credit}
         context.update(menu_product_view_context)
         return render(request,"credits.html",context)
         
class  CoupounAppliedView(LoginRequiredMixin,View):
    def get(self,request):
         user_obj=request.user
         context={"siteuser":user_obj,"coupouns":user_obj.customer.customercoupounapplied_set.all()}
         context.update(menu_product_view_context)
         return render(request,"coupouns.html",context)


class UserReviewList(LoginRequiredMixin,View):
    def get(self,request):
         user_obj=request.user
         context={"siteuser":user_obj,"reviews":user_obj.customer.review_set.all()}
         context.update(menu_product_view_context)
         return render(request,"user-reviews.html",context)

class UserOrderList(LoginRequiredMixin,View):
    def get(self,request):
          user_obj=request.user
          context={"siteuser":user_obj,"orders":user_obj.customer.order_set.all()}
          context.update(menu_product_view_context)
          return render(request,"user-orders.html",context)


#AJAX calls classes

#add to cart view
class PostGetCartView(View):
     """post and get products to cart"""
     CART_ID="CART_ID"
     def get(self,request): 
             cart=request.COOKIES.get(self.CART_ID)
             if cart:
                     new_cart_obj=Cart.objects.get(id=cart)
                     cart_items=new_cart_obj.cartitem_set.all()
                     cart_list=[]
                     for items in cart_items:
                         if items.coupon_code:
                            code=items.coupon_code
                            product_details={"Product_name":items.Product_In_Cart.Product_Name,
                                                             "Price":items.Total_Price(),
                                                             "Quantity":items.Product_Quantity,
                                                             "code":code,
                                                            }
                         else: 
                             product_details={"Product_name":items.Product_In_Cart.Product_Name,
                                                             "Price":items.Total_Price(),
                                                             "Quantity":items.Product_Quantity
                                                             }
                         cart_list.append(product_details)
                     return  JsonResponse(cart_list,safe=False)  
             else :
                     return  JsonResponse({"message":"no cookie present"})  
     def post(self,request):
             cart=request.COOKIES.get(self.CART_ID)
             if cart:
                 cart_obj=Cart.objects.get(pk=cart)
                 product=Product.objects.get(pk=request.POST["product"])
                 if cart_obj.cartitem_set.filter(Product_In_Cart=product).exists():
                       cart_obj.cartitem_set.filter(Product_In_Cart=product).update(Product_Quantity=request.POST["quantity"])
                 else:      
                       Cartitem.objects.create(Cart_Product_Belongs_To=cart_obj,Product_In_Cart=product,Product_Quantity=request.POST["quantity"])
                 response= JsonResponse({"message":"product data updated"},safe=False)  
             else:
                  new_cart_obj=Cart.objects.create(date_of_creation=timezone.now())
                  product=Product.objects.get(pk=request.POST["product"])
                  if product.Availiability:
                          Cartitem.objects.create(Cart_Product_Belongs_To=new_cart_obj,Product_In_Cart=product,Product_Quantity=request.POST["quantity"])
                          response= JsonResponse({"message":"cart made cookies on"}) 
                  else:
                          response=JsonResponse({"message":"product unavailable... unable to add"})         
                  response.set_cookie(self.CART_ID,new_cart_obj.pk)
             return response


class DeleteCartView(View):
     """delete product from cart"""
     CART_ID="CART_ID"
     def  post(self,request):
               cart=request.COOKIES.get(self.CART_ID)
               if cart:
                     product=Product.objects.get(pk=request.POST["product"])
                     Cartitem.objects.filter(Product_In_Cart=product).delete()
               else:
                      return JsonResponse({"message":"no cookie present"})
               return JsonResponse({"message":"product deleted"})

#yet to be tested
class ApplyCoupount(LoginRequiredMixin,View):
  CART_ID="CART_ID"
  def post(self,request):
        cart=request.COOKIES.get(self.CART_ID)
        if cart:
               cart_obj=Cart.objects.get(pk=cart)
               product=Product.objects.get(pk=request.POST["product"])
               coupon_code_entered=request.POST["coupon_entered"]
               if CouponCode.objects.filter(Code=coupon_code_entered).exist() and (not CustomerCouponUsedTrack.objects.filter(coupon_code=coupon_code_entered).exist()):
                    coupon=CouponCode.objects.get(Code=coupon_code_entered)
                    d_cart_item=cart_obj.cartitem_set.filter(Product_In_Cart=product)
                    if not(d.cart_item.coupon_code):
                       d_cart_item.coupon_code=coupon
                       d_cart_item.save()
                       return JsonResponse({"message":"coupon code applied"})         
               else :
                     return JsonResponse({"message":"coupon code expired"})
        else:
           return  JsonResponse({"response":"no cookie present"}) 

class RemoveCoupoun(LoginRequiredMixin,View):
    """removes coupon code"""
    pass



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

class PlaceOrder(LoginRequiredMixin,FormView):
     template_name="place-order.html"
     form_class=PlaceOrderForm
     #paytm redirect url
     success_url=""
     def get_context_data(self, **kwargs):
        context = super(PlaceOrder, self).get_context_data(**kwargs)
        context.update(menu_product_view_context)
        context["siteuser"]=self.request.user      
        return context 
     def form_valid(self,form):
           """make an  order"""
           print form.cleaned_data["Delivery_Type"]
           order=Order.objects.create( 
                                                 Order_In_Name_Of=form.cleaned_data["Order_In_Name_Of"],
                                                 Order_Customer=self.request.user.customer,
                                                 Order_Delivery_Type=Delivery_Type.objects.get(type=form.cleaned_data["Delivery_Type"]),
                                                 Order_Date_Time=timezone.now(),
                                                 Order_Address_Line1=form.cleaned_data["Order_Address_Line1"],
                                                 Order_Address_Line2=form.cleaned_data["Order_Address_Line2"],
                                                 Order_City=form.cleaned_data["Order_Region"],
                                                 Order_State="DELHI",
                                                 Order_ZIP=form.cleaned_data["Order_ZIP"],
                                                 Order_Payment_Type=OrderPaymentOptionCheck(form.cleaned_data["Payment_Method"]),
                                                 Order_Payment_status=Payment_Status.objects.get(payment_status="PENDING"),
                                                 Transaction_Id="null",
                                              )
           CART_ID="CART_ID"
           cart=self.request.COOKIES.get(CART_ID)
           if cart:
              cart_obj=Cart.objects.get(pk=cart)
              cart_items=cart_obj.cartitem_set.all()
              for cart_item in cart_items:
                   order_item=Order_Product_Specs.objects.create( 
                                                                              Order=order,
                                                                              Ordered_Product=cart_item.ProductAvailibiltyCheck(),
                                                                              Quantity=cart_item.Product_Quantity,
                                                                              Shipment_Authority=cart_item.Product_In_Cart.Shipment_Authority,
                                                                              Order_Reference=cart_item.OrderReferenceCheck(),
                                                                              Final_Ordered_Product_price=cart_item.Total_Price(),
                                                                              Order_Status=Order_Status_Model.objects.get(status_for_order="PLACED"),
                                                                               )
              # if(order.Order_Payment_Type.payment_type=="CASH ON DELIVERY"):
              #             messages.success(self.request, 'Order Placed succesfully')
              #             return super(PlaceOrder, self).form_valid(form)
              # else:
                         #redirect to paytm gateway
              return super(PlaceOrder, self).form_valid(form)


class OrderProcessCompleted(LoginRequiredMixin,View):
     pass
     #delete cart id and revive paytm crdentials



class CancelOrder(LoginRequiredMixin,View):
   """take ajax calls to cancel order with 
        order_id and order product as parameter in post request"""
   def post(self,request):
      pass
   

class AdminSignin(FormView):
    """admin login form and validation"""
    template_name="admin-login.html"
    form_class=SignInForm
    success_url="adminsite/panel"
    def form_valid(self,form):
           user=authenticate(self.request,username=form.cleaned_data["username"],password=form.cleaned_data["password"])
           if user is not None:
                 if user.is_active and user.is_superuser:
                     login(self.request,user)
                     return super(AdminSignin, self).form_valid(form)
                 else:
                       messages.error(self.request, 'Invalid username or password')
                       return redirect(reverse("admin-login"))    
           else:
               messages.error(self.request, 'Invalid username or password')
               return redirect(reverse("admin-login"))
                         

class AdminSignOut(LoginRequiredMixin,View):
    def get(self,request):
          logout(request)
          return redirect(reverse("admin-login"))

##admin panel
class AdminPanel(LoginRequiredMixin,UserPassesTestMixin,View):
     """admin panel landing page"""
     def test_func(self):
           return self.request.user.is_superuser
     def get(self,request):
        order_count=Order.objects.all().count()
        #ask for sales
        customer_count=Customer.objects.all().count()
        recent_order=Order.objects.all()[0:10]
        context={"order_count":order_count,"customer_count":customer_count,"recent_order":recent_order,"siteadmin":request.user}
        
        return render(request,"admin-index.html",context)      
































