# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#check for 404 in all views
from django.shortcuts import render,get_object_or_404
from django.views import View
from django.views.generic import DetailView,ListView
from .models import *
from django.http import Http404,JsonResponse,HttpResponse
from django.views.generic.edit import FormView
from .forms import *
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.core.urlresolvers  import reverse,reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .search import search
from .orderfilters import OrderFilter
from fpdf import FPDF
import os
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
os.environ["INVOICE_LANG"] = "en"

menu_product_view_context={
"base_category_list":BaseCategory.objects.all()
}

#use filter tems like term1+term2 in search_term filter
def ElasticSearch(request):
  if request.method=="GET":
    results=search(search_term=request.GET["search_term"])
    print (results)
    return render(request,"product-list.html",{"product_list":results})

class CustomView(ListView):
    model=BaseCategory
    context_object_name="base_category_list"
    template_name ="custom-product.html"
    def get_context_data(self, **kwargs):
        context = super(CustomView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
             context["siteuser"]=self.request.user
        return context

class HomeView(ListView):
    model=BaseCategory
    context_object_name="base_category_list"
    template_name ="index.html"
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        flash_sale=Flash_Sale.objects.filter(active=True)
        context["flash_sale"]=flash_sale
        if self.request.user.is_authenticated:
             context["siteuser"]=self.request.user
        return context

class ProductList(ListView):
  context_object_name="product_list"
  template_name="product-list.html"
  def get_queryset(self):
        try:
              return  Product.objects.filter(Product_Base_Category__Base_Slug_Field=self.kwargs["basefield"],product_Sub_Category__Sub_Category_Slug_Field=self.kwargs["subfield"])
        except:
              raise Http404
  def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context.update(menu_product_view_context)
        context.update({"filters":context["product_list"][0].product_Sub_Category.filter_name_set.all()})
        if self.request.user.is_authenticated:
             context["siteuser"]=self.request.user
        return context




class ProductDetails(DetailView):
   context_object_name="product"
   template_name="product-detail.html"
   def get_queryset(self):
        try:
            return  Product.objects.filter(Product_Base_Category__Base_Slug_Field=self.kwargs["basefield"],product_Sub_Category__Sub_Category_Slug_Field=self.kwargs["subfield"],pk=self.kwargs["pk"])
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
    def post(self,request):
           #print ("s")
           if "username" in request.POST:
                if CustomUser.objects.filter(username=request.POST["username"]).exists():
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
                                       City=form.cleaned_data["Region"],
                                       State="DELHI",
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
  success_url="/"
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
                 return "/"


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
    template_name="user-index.html"
    context_object_name = "siteuser"
    def get(self,request):
           context={"siteuser":request.user}
           context.update(menu_product_view_context)
           return render(request,self.template_name,context)

class  EditFormView(LoginRequiredMixin,FormView):
    """user edit details"""
    success_url="/user/user-dashboard/"
    template_name="user-edit-form.html"
    form_class=AccountEditForm
    def get_initial(self):
          user_obj=self.request.user
          initial={
                      "email":user_obj.customer.Customer_Email,
                      "contact_number":user_obj.customer.Customer_Contact_Number,
                      "address_line_1":user_obj.customer.Address_Line1,
                      "address_line_2":user_obj.customer.Address_Line2,
                      "Region":user_obj.customer.City,
                      "State":user_obj.customer.State,
                      "ZIP":user_obj.customer.ZIP,
                      }
          return initial

    def form_valid(self,form):
          user_obj=self.request.user
          Customer.objects.filter(User_customer=user_obj).update(
                                                        Customer_Email=form.cleaned_data["email"],
                                                        Address_Line1=form.cleaned_data["address_line_1"],
                                                        Address_Line2=form.cleaned_data["address_line_2"],
                                                        State="DELHI",
                                                        City=form.cleaned_data["Region"],
                                                        ZIP=form.cleaned_data["ZIP"],
                                                        Customer_Contact_Number=form.cleaned_data["contact_number"] )
          messages.success(self.request, 'Details Updated')
          return super(EditFormView, self).form_valid(form)

class SecurityView(LoginRequiredMixin,FormView):
    success_url="/user/user-dashboard/"
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
         context={"siteuser":user_obj,"coupouns":user_obj.customer.customercouponused_set.all()}
         context.update(menu_product_view_context)
         print context
         return render(request,"coupouns.html",context)


# class UserReviewList(LoginRequiredMixin,View):
#     def get(self,request):
#          user_obj=request.user
#          context={"siteuser":user_obj,"reviews":user_obj.customer.review_set.all()}
#          context.update(menu_product_view_context)
#          return render(request,"user-reviews.html",context)

class UserOrderList(LoginRequiredMixin,View):
    def get(self,request):
          user_obj=request.user
          context={"siteuser":user_obj,"orders":user_obj.customer.order_set.all()}
          context.update(menu_product_view_context)
          return render(request,"user-orders.html",context)


#AJAX calls classes
class AddToWishList(View,LoginRequiredMixin):
  def get(self,request):
    wish_obj=Wish_List.objects.get_or_create(User_Wishlist=request.user)
    product_list
    for products in wish_obj_set.all():
      product_list.append({"product name":products.Product_Name,
                           "product_url":product.get_product_url()
                            })
      return JsonResponse(product_list,safe=False)
  def post(self,request):
     wish_obj=Wish_List.objects.get_or_create(User_Wishlist=request.user)
     Wish_List_Product.objects.create(Wishlist=wish_obj,Product_In_Wishlist=request.POST.get("product_id"))
class DeleteFromWishList(View,LoginRequiredMixin):
   def post(self,request):
     if Wish_List_Product.objects.filter(pk=request.POST.get("product_id")).exists():
        Wish_List_Product.objects.filter(pk=request.POST.get("product_id")).delete()
        return JsonResponse({"message":"product removed"})
     else:
        return JsonResponse({"message":"does not exists"})

#add to cart view
class PostGetCartView(View):
     """post and get products to cart"""
     CART_ID="CART_ID"
     def get(self,request):
             cart=request.COOKIES.get(self.CART_ID)
             if cart:
                     cart_obj=Cart.objects.get(id=cart)
                     cart_items=cart_obj.cartitem_set.all()
                     cart_list=[]
                     for items in cart_items:
                        product_details={ "Product_name":items.Product_In_Cart.Product_Name,
                                           "Product_id":items.Product_In_Cart.pk,
                                           "Price":items.Total_Price(),
                                           "Quantity":items.Product_Quantity,
                                                        }
                        cart_list.append(product_details)
                     return  JsonResponse(cart_list,safe=False)
             else :
                     return  JsonResponse({"message":"no cookie present"})
     def post(self,request):

             cart=request.COOKIES.get(self.CART_ID)
             if cart:
                if Cart.objects.filter(pk=cart).exists():
                     cart_obj=Cart.objects.get(pk=cart)
                     product=Product.objects.get(pk=request.POST["product"])
                     if cart_obj.cartitem_set.filter(Product_In_Cart=product).exists():
                           cart_obj.cartitem_set.filter(Product_In_Cart=product).update(Product_Quantity=request.POST["quantity"])
                     else:
                           Cartitem.objects.create(Cart_Product_Belongs_To=cart_obj,Product_In_Cart=product,Product_Quantity=request.POST["quantity"])
                     response= JsonResponse({"message":"product data updated"},safe=False)
                else:
                   response =JsonResponse({"message":"cartid deleted"})
                   response.delete_cookie(self.CART_ID)
                   return response

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
class ApplyCoupon(View):
  CART_ID="CART_ID"
  def get(self,request):
        cart=request.COOKIES.get(self.CART_ID)
        if cart:
          cart_obj=Cart.objects.get(pk=cart)
          if cart_obj.coupon_code:
             return JsonResponse({"message":"coupon code already applied","value":cart_obj.coupon_code.Discount})
          else:
             return JsonResponse({"message":"coupon code not applied","value":0})
        else:
          return  JsonResponse({"alert":"something is wrong"})
  def post(self,request):
        cart=request.COOKIES.get(self.CART_ID)
        if cart:
          cart_obj=Cart.objects.get(pk=cart)
          if not(cart_obj.coupon_code):
               coupon_code_entered=request.POST["coupon_entered"]
               if (CouponCode.objects.filter(Code=coupon_code_entered).exists()):
                 coupon_code_entered=request.POST["coupon_entered"]
                 coupon=CouponCode.objects.get(Code=coupon_code_entered)
                 if (request.user.customer.usability) and (not(CustomerCouponUsed.objects.filter(coupon_code=coupon,customer_track=request.user.customer).exists())):
                    if not(cart_obj.coupon_code):
                       cart_obj.coupon_code=coupon
                       cart_obj.save()
                       return JsonResponse({"message":"coupon code applied","value":coupon.Discount})
                    else:
                       return JsonResponse({"message":"coupon code exist on this cart","value":coupon.Discount})
                 else:
                     return JsonResponse({"message":"coupon code not applicable","value":0})
               else :
                  return JsonResponse({"message":"coupon code not applicable","value":0})
          else:
            return JsonResponse({"message":"coupon code already applied","value":cart_obj.coupon_code.Discount})
                  
        else:
           return  JsonResponse({"alert":"something is wrong"})


class RemoveCoupoun(LoginRequiredMixin,View):
    """removes coupon code"""
    pass


class CheckoutView(LoginRequiredMixin,View):
     CART_ID="CART_ID"
     def get(self,request):
            cart=request.COOKIES.get(self.CART_ID)
            if cart:
                 user=request.user
                 if Cart.objects.filter(pk=cart).exists():
                       cart_obj=Cart.objects.get(pk=cart)
                       context={"siteuser":user,"cart_obj":cart_obj}
                       return render(request,"checkout.html",context)
                 else:
                       messages.error(self.request, 'no cart')
                       response =redirect(reverse("home"))
                       response.delete_cookie("CART_ID")
                       return response
            else:
                #disable checkout button
                messages.error(self.request, 'nothing in cart')
                return  redirect(reverse("home"))




# class PlaceOrder(LoginRequiredMixin,FormView):
#      template_name="place-order.html"
#      form_class=PlaceOrderForm
#      #paytm redirect url
#      success_url="user/orders/"
#      def get_context_data(self, **kwargs):
#         context = super(PlaceOrder, self).get_context_data(**kwargs)
#         context.update(menu_product_view_context)
#         context["siteuser"]=self.request.user
#         return context
#      def form_valid(self,form):
#            """make an  order"""
#            #print (form.cleaned_data["Delivery_Type"])
#            order=Order.objects.create(
#                                                  Order_In_Name_Of=form.cleaned_data["Order_In_Name_Of"],
#                                                  Order_Customer=self.request.user.customer,
#                                                  Order_Delivery_Type=Delivery_Type.objects.get(type=form.cleaned_data["Delivery_Type"]),
#                                                  Order_Date_Time=timezone.now(),
#                                                  Order_Address_Line1=form.cleaned_data["Order_Address_Line1"],
#                                                  Order_Address_Line2=form.cleaned_data["Order_Address_Line2"],
#                                                  Order_City=form.cleaned_data["Order_Region"],
#                                                  Order_State="DELHI",
#                                                  Order_ZIP=form.cleaned_data["Order_ZIP"],
#                                                  Order_Payment_Type=OrderPaymentOptionCheck(form.cleaned_data["Payment_Method"]),
#                                                  Order_Payment_status=Payment_Status.objects.get(payment_status="PENDING"),
#                                                  Transaction_Id="null",
#                                               )
#            CART_ID="CART_ID"
#            cart=self.request.COOKIES.get(CART_ID)
#            if cart:
#               if Cart.objects.filter(pk=cart).exists():
#                     cart_obj=Cart.objects.get(pk=cart)
#                     cart_items=cart_obj.cartitem_set.all()
#                     for cart_item in cart_items:
#                          order_item=Order_Product_Specs.objects.create(
#                                                                                     Order=order,
#                                                                                     Ordered_Product=cart_item.ProductAvailibiltyCheck(),
#                                                                                     Quantity=cart_item.Product_Quantity,
#                                                                                     Shipment_Authority=cart_item.Product_In_Cart.Shipment_Authority,
#                                                                                     Order_Reference=cart_item.OrderReferenceCheck(),
#                                                                                     Final_Ordered_Product_price=cart_item.Total_Price(),
#                                                                                     Order_Status=Order_Status_Model.objects.get(status_for_order="PLACED"),
#                                                                                      )
#               else:
#                  messages.error(self.request, 'no cart')
#                  response = redirect(reverse("home"))
#                  response.delete_cookie(CART_ID)
#                  return response
#               return super(PlaceOrder, self).form_valid(form)
#            else:
#                 messages.error(self.request, 'nothing in cart')
#                 return redirect(reverse("home"))


class PlaceOrder(LoginRequiredMixin,FormView):
     template_name="place-order.html"
     form_class=PlaceOrderForm
     #paytm redirect url

     def get_success_url(self,**kwargs):
        return reverse_lazy("order-payment",kwargs={"order_id":kwargs["order_id"]})
     def get_context_data(self, **kwargs):
        context = super(PlaceOrder, self).get_context_data(**kwargs)
        context.update(menu_product_view_context)
        context["siteuser"]=self.request.user
        return context
     def form_valid(self,form):
           """make an  order"""
           CART_ID="CART_ID"
           cart=self.request.COOKIES.get(CART_ID)
           if cart:
              if Cart.objects.filter(pk=cart).exists():
                    cart_obj=Cart.objects.get(pk=cart)
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
                                                 Transaction_Id="",
                                                 Order_Reference=cart_obj.OrderReferenceCheck()
                                                        )
                    cart_items=cart_obj.cartitem_set.all()
                    for cart_item in cart_items:
                         order_item=Order_Product_Specs.objects.create(
                                                                      Order=order,
                                                                      Ordered_Product=cart_item.ProductAvailibiltyCheck(),
                                                                      Quantity=cart_item.Product_Quantity,
                                                                      Shipment_Authority_Details=cart_item.Product_In_Cart.Shipment_Authority,
                                                                      Final_Ordered_Product_price=cart_item.Total_Price(),
                                                                      Order_Status=Order_Status_Model.objects.get(status_for_order="PENDING"),
                                                                        )
              else:
                 messages.error(self.request, 'no cart')
                 response = redirect(reverse("home"))
                 response.delete_cookie(CART_ID)
                 return response
              return redirect(self.get_success_url(order_id=order.pk))
           else:
                messages.error(self.request, 'nothing in cart')
                return redirect(reverse("home"))


class OrderPayment(LoginRequiredMixin,View):
  def get(self,request,order_id):
    user_obj=request.user
    order=Order.objects.get(pk=order_id)
    if (order.Order_Payment_status.payment_status=="PENDING") and (order.Transaction_Id=="") and(order.Order_Customer==request.user.customer):
        return render(request,"order-payment.html",{"siteuser":user_obj,"order":order})
    else:
      raise Http404
  def post(self,request,order_id):
    """usablity cancel"""
    CART_ID="CART_ID"
    if Order.objects.filter(pk=order_id).exists():
       order=Order.objects.get(pk=order_id)
       """just mark cancel here the whole order will be termed as cancel"""
       if (order.Order_Payment_status.payment_status=="PENDING") and (order.Transaction_Id=="") and(order.Order_Customer==request.user.customer):
            Order.objects.filter(pk=order_id).update(Transaction_Id=request.POST.get("transaction_id"))
            cart=request.COOKIES.get(CART_ID)
            if cart:
              cart_obj=Cart.objects.get(pk=cart)
              if cart_obj.coupon_code:
                  CustomerCouponUsed.objects.create(customer_track=request.user.customer,coupon_code=cart_obj.coupon_code)
                  if request.user.customer.usability==True:
                      request.user.customer.usability=False
                  else:
                      request.user.customer.usability
              Cart.objects.filter(pk=cart).delete()
              print "dsds"
              response = redirect(reverse("user-orders"))
              response.delete_cookie(CART_ID)
              return response
            else:
              return redirect(reverse("user-orders"))             
       else:
         raise Http404
    else:
      raise Http404
    


class OrderProcessCompleted(LoginRequiredMixin,View):
     pass
     #delete cart id and revive paytm crdentials and dadd coupon to used



class CancelOrder(LoginRequiredMixin,View):
   """take ajax calls to cancel order with
        order_id and order_product_id as parameter in post request"""
   def post(self,request):
        order=request.POST.get("order_id")
        order_obj=get_object_or_404(Order,pk=order)
        if (request.user==order_obj.Order_Customer.User_customer):
          if ((timezone.now()-timezone.timedelta(days=1))<order_obj.Order_Date_Time):
             order_items_id=request.POST.getlist("order_product_id")
             for product_id in order_items_id:
                  order_product=get_object_or_404(Order_Product_Specs,pk=product_id)
                  if order_product.Order_Status.status_for_order=="DELIVERED":
                     messages.error(self.request, 'order delivered')
                     return redirect(reverse("user-orders"))
                  else:
                     print("I am cancelling") 
                     order_product.Order_Status=Order_Status_Model.objects.get(status_for_order="CANCELLED")
                     order_product.save()
          else:
              messages.error(self.request, 'request timeout')
              return redirect(reverse("user-orders"))
        else:
            return  HttpResponse(status=401)
        return redirect(reverse("user-orders"))

class AdminSignin(FormView):
    """admin login form and validation"""
    template_name="admin-login.html"
    form_class=SignInForm
    success_url="/admin-panel/"
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

        return render(request,"admin-home.html",context)



class AdminBaseCategory(LoginRequiredMixin,UserPassesTestMixin,View):
     """base categoty handling"""
     def test_func(self):
           return self.request.user.is_superuser
     def get(self,request):
         base_category=BaseCategory.objects.all()
         paginator = Paginator(base_category, 25)
         page = request.GET.get('page')
         try:
            contacts = paginator.page(page)
         except PageNotAnInteger:
            contacts = paginator.page(1)
         except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
         return render(request, 'admin-catalog-base-category.html', {'contacts':contacts})



class AdminBasecategoryCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
   model = BaseCategory
   fields = ["Base_Category","Base_Category_Pic"]
   template_name="admin-base-category-edit.html"
   success_url="/admin-panel/catalog/basecategories/"
   def test_func(self):
           return self.request.user.is_superuser

class AdminBasecategoryUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
   model = BaseCategory
   fields = ["Base_Category","Base_Category_Pic"]
   template_name="admin-base-category-edit.html"
   success_url="/admin-panel/catalog/basecategories/"
   def test_func(self):
           return self.request.user.is_superuser

class AdminBasecategoryDeleteView(LoginRequiredMixin,UserPassesTestMixin,View):
      def test_func(self):
           return self.request.user.is_superuser
      def post(self,request):
             for id in  request.POST.getlist("selected"):
                  BaseCategory.objects.filter(pk=id).delete()
                  messages.success(self.request, 'Base Category Deleted')
             return redirect(reverse("admin-catalog-base"))

class AdminSubCategory(LoginRequiredMixin,UserPassesTestMixin,View):
     """sub categoty handling"""
     def test_func(self):
           return self.request.user.is_superuser
     def get(self,request):
         sub_category=SubCategory.objects.all()
         paginator = Paginator(sub_category, 25)
         page = request.GET.get('page')
         try:
            contacts = paginator.page(page)
         except PageNotAnInteger:
            contacts = paginator.page(1)
         except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
         return render(request, 'admin-catalog-sub-category.html', {'contacts':contacts})

class AdminSubcategoryCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
   """admin sub category form handling"""
   model=SubCategory
   template_name="admin-sub-category-edit.html"
   success_url="/admin-panel/catalog/subcategories/"
   fields=["Base_category_Key","Sub_Category","Sub_Category_Pic"]
   def test_func(self):
           return self.request.user.is_superuser

class AdminSubcategoryUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
   """admin sub category form handling"""
   model=SubCategory
   template_name="admin-sub-category-edit.html"
   fields=["Base_category_Key","Sub_Category","Sub_Category_Pic"]
   success_url="/admin-panel/catalog/subcategories/"
   def test_func(self):
           return self.request.user.is_superuser


class AdminSubcategoryDeleteView(LoginRequiredMixin,UserPassesTestMixin,View):
      def test_func(self):
           return self.request.user.is_superuser
      def post(self,request):
             for id in  request.POST.getlist("selected"):
                  SubCategory.objects.filter(pk=id).delete()
                  messages.success(self.request, 'Sub Category Deleted')
             return redirect(reverse("admin-catalog-sub"))


class AdminProduct(LoginRequiredMixin,UserPassesTestMixin,View):
     """sub categoty handling"""
     def test_func(self):
           return self.request.user.is_superuser
     def get(self,request):
         products=Product.objects.all()
         paginator = Paginator(products, 25)
         page = request.GET.get('page')
         try:
            contacts = paginator.page(page)
         except PageNotAnInteger:
            contacts = paginator.page(1)
         except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
         return render(request, 'admin-catalog-product.html', {'contacts':contacts})

class AdminProductCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
   """admin sub category form handling"""
   model=Product
   template_name="admin-product-edit.html"
   success_url="/admin-panel/catalog/products/"
   fields=["Product_Base_Category","product_Sub_Category","Product_Name","Discount","Base_Price","Availiability","Description","Features","TechnicalSpecs","Main_Image","Shipment_Authority","TaxOnProduct"]
   def test_func(self):
           return self.request.user.is_superuser

class AdminProductUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
   """admin sub category form handling"""
   model=Product
   template_name="admin-product-edit.html"
   fields=["Product_Base_Category","product_Sub_Category","Product_Name","Discount","Base_Price","Availiability","Description","Features","TechnicalSpecs","Main_Image","Shipment_Authority"]
   success_url="/admin-panel/catalog/products/"
   def test_func(self):
           return self.request.user.is_superuser


class AdminProductDeleteView(LoginRequiredMixin,UserPassesTestMixin,View):
      def test_func(self):
           return self.request.user.is_superuser
      def post(self,request):
             for id in  request.POST.getlist("selected"):
                  Product.objects.filter(pk=id).delete()
                  messages.success(self.request, 'Product Deleted')
             return redirect(reverse("admin-catalog-product"))

class AdminProductPics(LoginRequiredMixin,UserPassesTestMixin,View):
     """sub categoty handling"""
     def test_func(self):
           return self.request.user.is_superuser
     def get(self,request):
         pics=Pics.objects.all()
         paginator = Paginator(pics, 25)
         page = request.GET.get('page')
         try:
            contacts = paginator.page(page)
         except PageNotAnInteger:
            contacts = paginator.page(1)
         except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
         return render(request, 'admin-catalog-product-pics.html', {'contacts':contacts})

class AdminProductPicsCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
   """admin sub category form handling"""
   model=Pics
   template_name="admin-product-pics-edit.html"
   success_url="/admin-panel/catalog/products-pics/"
   fields=["ProductPics","Images"]
   def test_func(self):
           return self.request.user.is_superuser

class AdminProductPicsUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
   """admin sub category form handling"""
   model=Pics
   template_name="admin-product-pics-edit.html"
   fields=["ProductPics","Images"]
   success_url="/admin-panel/catalog/products-pics/"
   def test_func(self):
           return self.request.user.is_superuser


class AdminProductPicsDeleteView(LoginRequiredMixin,UserPassesTestMixin,View):
      def test_func(self):
           return self.request.user.is_superuser
      def post(self,request):
             for id in  request.POST.getlist("selected"):
                  Pics.objects.filter(pk=id).delete()
                  messages.success(self.request, 'Pic Deleted')
             return redirect(reverse("admin-catalog-product-pics"))

class AdminSellers(LoginRequiredMixin,UserPassesTestMixin,View):
     """sellers handling"""
     def test_func(self):
           return self.request.user.is_superuser
     def get(self,request):
         seller=Seller.objects.all()
         paginator = Paginator(seller, 25)
         page = request.GET.get('page')
         try:
            contacts = paginator.page(page)
         except PageNotAnInteger:
            contacts = paginator.page(1)
         except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
         return render(request, 'admin-customer-sellers.html', {'contacts':contacts})

class AdminSellersCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
   """admin sub category form handling"""
   model=Seller
   template_name="admin-customer-sellers-edit.html"
   success_url="/admin-panel/customer/sellers/"
   fields=["Seller_Id","Seller_Name","Address","Profile","email","Contact_Number"]
   def test_func(self):
           return self.request.user.is_superuser

class AdminSellersUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
   """admin sub category form handling"""
   model=Seller
   template_name="admin-customer-sellers-edit.html"
   fields=["Seller_Id","Seller_Name","Address","Profile","email","Contact_Number"]
   success_url="/admin-panel/customer/sellers/"
   def test_func(self):
           return self.request.user.is_superuser


class AdminSellersDeleteView(LoginRequiredMixin,UserPassesTestMixin,View):
      def test_func(self):
           return self.request.user.is_superuser
      def post(self,request):
             for id in  request.POST.getlist("selected"):
                  Seller.objects.filter(pk=id).delete()
                  messages.success(self.request, 'Pic Deleted')
             return redirect(reverse("admin-customer-sellers"))

class AdminCustomer(LoginRequiredMixin,UserPassesTestMixin,View):
     """sellers handling"""
     def test_func(self):
           return self.request.user.is_superuser
     def get(self,request):
         customer=Customer.objects.all()
         paginator = Paginator(customer, 25)
         page = request.GET.get('page')
         try:
            contacts = paginator.page(page)
         except PageNotAnInteger:
            contacts = paginator.page(1)
         except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
         return render(request, 'admin-customer-enduser.html', {'contacts':contacts})


class AdminCoupon(LoginRequiredMixin,UserPassesTestMixin,View):
     """sellers handling"""
     def test_func(self):
           return self.request.user.is_superuser
     def get(self,request):
         coupon=CouponCode.objects.all()
         paginator = Paginator(coupon, 25)
         page = request.GET.get('page')
         try:
            contacts = paginator.page(page)
         except PageNotAnInteger:
            contacts = paginator.page(1)
         except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
         return render(request, 'admin-marketing-coupon.html', {'contacts':contacts})

class AdminCouponCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
   """admin sub category form handling"""
   model=CouponCode
   template_name="admin-marketing-coupon-edit.html"
   success_url="/admin-panel/marketing/coupon/"
   fields=["Code","Sales_Member","Discount"]
   def test_func(self):
           return self.request.user.is_superuser

class AdminCouponUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
   """admin sub category form handling"""
   model=CouponCode
   template_name="admin-marketing-coupon-edit.html"
   fields=["Code","Sales_Member","Discount"]
   success_url="/admin-panel/marketing/coupon/"
   def test_func(self):
           return self.request.user.is_superuser


class AdminCouponDeleteView(LoginRequiredMixin,UserPassesTestMixin,View):
      def test_func(self):
           return self.request.user.is_superuser
      def post(self,request):
             for id in  request.POST.getlist("selected"):
                  CouponCode.objects.filter(pk=id).delete()
                  messages.success(self.request, 'Pic Deleted')
             return redirect(reverse("admin-marketing-coupon"))


#####order stuff admin
class AdminOrderView(LoginRequiredMixin,UserPassesTestMixin,View):
    def test_func(self):
        return self.request.user.is_superuser
    def get(self,request):
         filter = OrderFilter(request.GET, queryset=Order.objects.all())
         status=Order_Status_Model.objects.all()
         order_list=Order.objects.all()

         paginator = Paginator(order_list, 25)
         page = request.GET.get('page')

         try:
            contacts = paginator.page(page)
         except PageNotAnInteger:
            contacts = paginator.page(1)
         except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
         return render(request,"admin-order-list.html",{"contacts":contacts,"status":status,'filter': filter})

# admin order view to show all the categories
class AdminOrderViewByCategory(LoginRequiredMixin,UserPassesTestMixin,View):
    def test_func(self):
        return self.request.user.is_superuser
    def get(self,request):
         sub_category=SubCategory.objects.all()
         paginator = Paginator(sub_category, 25)
         page = request.GET.get('page')
         try:
            contacts = paginator.page(page)
         except PageNotAnInteger:
            contacts = paginator.page(1)
         except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
         return render(request, 'admin-order-categories.html', {'contacts':contacts})

#admin order list for selected category
class AdminOrderViewByGivenCategory(LoginRequiredMixin,UserPassesTestMixin,View):
    def test_func(self):
        return self.request.user.is_superuser
    def get(self,request,**kwargs):
         
         status=Order_Status_Model.objects.all()
         
         order_list=Order.objects.all()
         required_orders = order_list
         to_be_deleted = []
         for order in order_list:
               found = False
               products = order.order_product_specs_set.all()
               for product in products:
                     current_sub_category = product.Ordered_Product.product_Sub_Category
                     if(current_sub_category.Sub_Category == self.kwargs["subfield"]):
                           found = True
                           break
               print(found)
               if not found:
                  # required_orders=required_orders.filter(pk = order.pk).delete()
                  to_be_deleted.append(order.pk)

         print(to_be_deleted)         
         required_orders = Order.objects.exclude(pk__in = to_be_deleted)   
         filter = OrderFilter(request.GET, queryset=required_orders)
         print(required_orders)
         paginator = Paginator(required_orders, 25)
         
         page = request.GET.get('page')

         try:
            contacts = paginator.page(page)
         except PageNotAnInteger:
            contacts = paginator.page(1)
         except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
         return render(request,"admin-order-list.html",{"contacts":contacts,"status":status,'filter': filter})

class WholeOrderPaymentConfirm(LoginRequiredMixin,UserPassesTestMixin,View):
    def test_func(self):
        return self.request.user.is_superuser
    def post(self,request):
       order_id=request.POST.get("order_id")
       if Order.objects.filter(pk=order_id).exists():
        order=Order.objects.get(pk=order_id)
        if request.POST.get("payment_status")=="COMPLETED":
          if order.Order_Payment_status.payment_status=="PENDING":
            order.Order_Payment_status=Payment_Status.objects.get(payment_status="COMPLETED")
            order.Transaction_Id=request.POST.get("transactionID")
            #order reference
            client = Client(request.user.customer.Customer_First_Name)
            provider = Provider('Fashvolts')
            creator = Creator('Vaibhav')
            invoice = Invoice(client, provider, creator)
            invoice.currency=u'Rs.'

            for product in order.order_product_specs_set.all():
              product.Order_Status=Order_Status_Model.objects.get(status_for_order="PLACED")
              #shipment id enter
              invoice.add_item(Item(product.Quantity, product.Final_Ordered_Product_price, description=product.Ordered_Product.Product_Name))
            pdf = SimpleInvoice(invoice)
            name="invoice"+str(order.pk)
            order.Invoice=pdf.gen(name, generate_qr_code=False)
            order.save()
            return JsonResponse({"status":"order made"})

        else:
          if order.Order_Payment_status.payment_status=="CANCELLED":
            order.Order_Payment_status=Payment_Status.objects.get(payment_status="CANCELLED")
            for product in order.order_product_specs_set.all():
              product.Order_Status=Order_Status_Model.objects.get(status_for_order="CANCELLED")
            return JsonResponse({"status":"order cancelled"})  


                
        
class OrderProductStatusChange(LoginRequiredMixin,UserPassesTestMixin,View):
  """ use  order_product_id and order_id """
  def test_func(self):
        return self.request.user.is_superuser
  def post(self,request):
       order_id=request.POST.get("order_id")
       print (order_id)
       if Order.objects.filter(pk=order_id).exists():
          order=Order.objects.get(pk=order_id)
          product_id=request.POST.get("order_product_id")
          ordered_product=Order_Product_Specs.objects.get(pk=product_id)
          ordered_product.Order_Status=Order_Status_Model.objects.get(status_for_order=request.POST.get("status"))
          ordered_product.save()
          return JsonResponse({"message":"status changed"})
       else:
          return JsonResponse({"message":"order does not exist"})


#admin reports stuff ------------------------------------------->

class AdminReportsOrderView(LoginRequiredMixin,UserPassesTestMixin,View):
    def test_func(self):
        return self.request.user.is_superuser
    def get(self,request):
         #filter = OrderFilter(request.GET, queryset=Order.objects.all())
         status=Order_Status_Model.objects.all()
         order_list=Order.objects.all()

         
         return render(request,"admin-reports-orders.html",{"contacts":order_list,"status":status}) 

class AdminReportsUserView(LoginRequiredMixin,UserPassesTestMixin,View):
    def test_func(self):
        return self.request.user.is_superuser
    def get(self,request):
         #filter = OrderFilter(request.GET, queryset=Order.objects.all())
         #status=Order_Status_Model.objects.all()
         customer_list=Customer.objects.all()

         
         return render(request,"admin-reports-users.html",{"contacts":customer_list}) 
      

#api for object returns for different reports
 
class OrderReportApi(LoginRequiredMixin,UserPassesTestMixin,View):
      def test_func(self):
        return self.request.user.is_superuser
      def get(self,request):
            orders = Order.objects.all()
            response_data = {}
            prev_date = orders[0].Order_Date_Time.date()
            count = 0
            index = 0
            for order in orders:
                  if(order.Order_Date_Time.date() == prev_date):
                        count = count+1
                  else:
                        current_entry = {
                              "x": order.Order_Date_Time.date(),
                              "y": count
                        }
                        response_data[index]=current_entry
                        index=index+1
                        count = 0
                        prev_date = order.Order_Date_Time
           
            # if the response is empty because every order is on same date and it never goes in else of for loop
            if not response_data:
                  current_entry = {
                              "x": order.Order_Date_Time.date(),
                              "y": count
                        }
                  response_data[index]=current_entry

            return JsonResponse(response_data)                  

#user report api
class UserReportApi(LoginRequiredMixin,UserPassesTestMixin,View):
      def test_func(self):
        return self.request.user.is_superuser
      def get(self,request):
            users = Customer.objects.all()
            response_data = {}
            prev_date = users[0].Join_Date_Time.date()
            count = 0
            index = 0
            for order in users:
                  if(order.Join_Date_Time.date() == prev_date):
                        count = count+1
                  else:
                        current_entry = {
                              "x": order.Join_Date_Time.date(),
                              "y": count
                        }
                        response_data[index]=current_entry
                        index=index+1
                        count = 0
                        prev_date = order.Join_Date_Time
           
            # if the response is empty because every order is on same date and it never goes in else of for loop
            if not response_data:
                  current_entry = {
                              "x": order.Join_Date_Time.date(),
                              "y": count
                        }
                  response_data[index]=current_entry

            return JsonResponse(response_data)                  


#sales panel stuff----------------------------------------------->
class SalesSignin(FormView):
    """sales login form and validation"""
    template_name="sales-login.html"
    form_class=SignInForm
    success_url="/sales-panel/"
    def form_valid(self,form):
           user=authenticate(self.request,username=form.cleaned_data["username"],password=form.cleaned_data["password"])
           if Sales_Team.objects.filter(Sales_user__username=form.cleaned_data["username"]).exists():
               if user is not None:
                     if user.is_active:
                         login(self.request,user)
                         return super(SalesSignin, self).form_valid(form)
                     else:
                           messages.error(self.request, 'Invalid username or password')
                           return redirect(reverse("sales-signin"))
               else:
                   messages.error(self.request, 'Invalid username or password')
                   return redirect(reverse("sales-signin"))
           else:
               messages.error(self.request, 'Invalid username or password')
               return redirect(reverse("sales-signin"))





class SalesPanel(LoginRequiredMixin,UserPassesTestMixin,View):
  """sales panel"""
  def test_func(self):
     return Sales_Team.objects.filter(Sales_user=self.request.user).exists()
  def get(self,request):
      """sales panel landing page"""
      coupon_used_list=[]
      sales=Sales_Team.objects.get(Sales_user=request.user)
      for code in sales.couponcode_set.all():
         if CustomerCouponUsedTrack.objects.filter(coupon_code=code).exists():
             coupon_used=CustomerCouponUsedTrack.objects.filter(coupon_code=code)
             coupon_used_list.append(coupon_used)
      return render(request,"sales-index.html",{"sales":sales,"coupon_used_list":coupon_used_list})


class SalesSignOut(LoginRequiredMixin,View):
    def get(self,request):
          logout(request)
          return redirect(reverse("sales-signin"))

#seller stuff-------------------------->
# class SellerPanel(LoginRequiredMixin,UserPassesTestMixin,View):
#   """sales panel"""
#   def test_func(self):
#       return Seller.objects.filter(seller_user=self.request.user).exists()
#   def get(self,request):
#       """seller panel landing page"""
#       seller=Seller.objects.get(seller_user=request.user)
#       return render(request,"seller-panel.html",{"seller":seller})

# class SellerSignin(FormView):
#     """sales login form and validation"""
#     template_name="seller-login.html"
#     form_class=SignInForm
#     success_url="sellersite/panel"
#     def form_valid(self,form):
#            user=authenticate(self.request,username=form.cleaned_data["username"],password=form.cleaned_data["password"])
#            if Seller.objects.filter(seller_user__username=form.cleaned_data["username"]).exists():
#                if user is not None:
#                      if user.is_active:
#                          login(self.request,user)
#                          return super(SellerSignin, self).form_valid(form)
#                      else:
#                            messages.error(self.request, 'Invalid username or password')
#                            return redirect(reverse("seller-signin"))
#                else:
#                    messages.error(self.request, 'Invalid username or password')
#                    return redirect(reverse("seller-signin"))
#            else:
#                messages.error(self.request, 'Invalid username or password')
#                return redirect(reverse("seller-signin"))

# class SellerSignOut(LoginRequiredMixin,View):
#     def get(self,request):
#           logout(request)
#           return redirect(reverse("seller-signin"))

# class SellerProductAdd(LoginRequiredMixin,CreateView,UserPassesTestMixin):
#    model=Product
#    template_name="seller-product-cu.html"
#    fields="__all__"
#    success_url="sellersite/panel"
#    def test_func(self):
#       return Seller.objects.filter(seller_user=self.request.user).exists()

# class SellerProductUpdate(LoginRequiredMixin,UpdateView,UserPassesTestMixin):
#    model=Product
#    fields="__all__"
#    template_name="seller-product-cu.html"
#    success_url="sellersite/panel"
#    def test_func(self):
#       return Seller.objects.filter(seller_user=self.request.user).exists()

# class SellerProductDelete(LoginRequiredMixin,DeleteView,UserPassesTestMixin):
#    model=Product
#    success_url="sellersite/panel"
#    def test_func(self):
#       return Seller.objects.filter(seller_user=self.request.user).exists()


class CustomModule(ListView):
  context_object_name="brands"
  model=Brand
  template_name="custom-module-index.html"

@login_required
def getphones(request,brand_slug):
  """js ajax call display all phone 
     names of that brand"""
  phones=Phones.objects.filter(brand__slug=brand_slug)
  phone_list=[]
  for phone in phones:
    phone_list.append({phone.pk:phone.name})
  return JsonResponse(phone_list,safe=False)

class CustomeModuleMain(LoginRequiredMixin,View):
  def get(self,request,pk):
     phone_obj=Phones.objects.get(pk=pk)
     return render(request,"custom-main.html",{"phone":phone_obj})    
class PostCustomModule(View):
   def post(self,request):
      """first call this then this would return product id and make an add to cart post call using its result"""
      if request.user.customer.can_create_custom:
        base_price=200
        product=Product.objects.create(
                        Product_Base_Category=BaseCategory.objects.get( Base_Category="CUSTOM"),
                        product_Sub_Category=SubCategory.objects.get(Sub_Category="PHONE COVERS"),
                        Product_Name=request.POST["name"]+str(pk),
                        Base_Price=base_price,
                        Main_Image=request.FILE["custom_image"],
                        is_displayed=request.POST["choice"],
                        Product_Seller=Seller.objects.get(Seller_Name="FashVolts"),
                        TaxOnProduct=Tax.objects.get(Tax_Percentage=17),
                        Shipment_Authority=Shipment_Orgs.objects.get(Shipping_Company_Name="Fashvolts")
                         )
        return JsonResponse({"product":product.pk,"quantity":1})
      else:
         raise Http404   

                      
 

