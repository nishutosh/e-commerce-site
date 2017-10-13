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
from django.core.urlresolvers  import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .search import search
from .orderfilters import OrderFilter
menu_product_view_context={
"base_category_list":BaseCategory.objects.all() 
}

#use filter tems like term1+term2 in search_term filter 
def ElasticSearch(request):
  if request.method=="GET":
    results=search(search_term=request.GET["search_term"])
    print results
    return render(request,"product_list.html",{"product_list":results})

    

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
  template_name="product_list.html"
  def get_queryset(self):
        try: 
              return  Product.objects.filter(is_displayed=True,Product_Base_Category__Base_Slug_Field=self.kwargs["basefield"],product_Sub_Category__Sub_Category_Slug_Field=self.kwargs["subfield"])
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
   template_name="product.html"
   def get_queryset(self):
        try:
            return  Product.objects.filter(is_displayed=True,Product_Base_Category__Base_Slug_Field=self.kwargs["basefield"],product_Sub_Category__Sub_Category_Slug_Field=self.kwargs["subfield"],pk=self.kwargs["pk"])
        except:
            raise Http404
   def get_context_data(self, **kwargs):
        context = super(ProductDetails, self).get_context_data(**kwargs)
        context["pics"]=context["product"].pics_set.all()
        context["review"]=Review.objects.all()
        context.update(menu_product_view_context)
        if self.request.user.is_authenticated:
             context["siteuser"]=self.request.user      
        return context 

class UserNameCheckView(View):
    """checks username exist or not during registartion process"""
    def post(self,request):
           print "s"
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


class ReviewSubmitView(LoginRequiredMixin,View):
    def post(self,request):
        """user submit review"""
        if request.POST.get("review_id")=="new":
            Review.objects.create(Reviewer=self.request.user,
                                   Product=request.POST.get["product"],
                                   Review_Title=request.POST.get["Review_titile"],
                                   Review_Body=request.POST.get["Review_Body"],
                                   show_review=True)       
            return JsonResponse({"message":"review submitted"})
        else:
            if Review.objects.filter(pk=request.Post.get("review_id")).exists():
               Review.objects.filter(pk=request.Post.get("review_id")).update(Review_Title=request.POST.get("review_title"),Review_Body=request.POST.get("review_body"))
               return JsonResponse({"message":"review updated"})
            else:
               return JsonResponse({"message":"review does not exist"}) 


class ReviewDelete(LoginRequiredMixin,View):
    def post(self,request):
       if Review.objects.filter(pk=request.POST.get("review_id")).exists():
           Review.objects.filter(pk=request.POST.get("review_id")).delete()
           return JsonResponse({"message":"review deleted"})
       else:
           return JsonResponse({"message":"review does not exist"})

            



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
                      "Region":user_obj.customer.City,
                      "ZIP":user_obj.customer.ZIP,
                      }
          return initial

    def form_valid(self,form):
          user_obj=self.request.user
          Customer.objects.filter(User_customer=user_obj).update(
                                                        Customer_Email=form.cleaned_data["email"],
                                                        Address_Line1=form.cleaned_data["address_line_1"],
                                                        Address_Line2=form.cleaned_data["address_line_2"],
                                                        City=form.cleaned_data["Region"],
                                                        State="DELHI",
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
                            code=items.coupon_code.Code
                            product_details={ "Product_name":items.Product_In_Cart.Product_Name,
                                                             "Product_id":items.Product_In_Cart.pk,
                                                             "Price":items.Total_Price(),
                                                             "Quantity":items.Product_Quantity,
                                                             "code":code,
                                                             "discount":items.coupon_code.Discount,
                                                            }
                         else: 
                             product_details={"Product_name":items.Product_In_Cart.Product_Name,
                                                             "Product_id":items.Product_In_Cart.pk,
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
class ApplyCoupon(View):
  CART_ID="CART_ID"
  def post(self,request):
        cart=request.COOKIES.get(self.CART_ID)
        if cart:
               cart_obj=Cart.objects.get(pk=cart)
               product=Product.objects.get(pk=request.POST["product"])
               coupon_code_entered=request.POST["coupon_entered"]
               if CouponCode.objects.filter(Code=coupon_code_entered).exists() and (not CustomerCouponUsedTrack.objects.filter(coupon_code__Code=coupon_code_entered).exists()):
                    coupon=CouponCode.objects.get(Code=coupon_code_entered)
                    if not(cart_obj.cartitem_set.filter(Product_In_Cart=product,coupon_code=coupon).exists()):
                       d_cart_item=cart_obj.cartitem_set.get(Product_In_Cart=product)
                       d_cart_item.coupon_code=coupon
                       d_cart_item.save()
                       return JsonResponse({"message":"coupon code applied"})
                    else:
                       return JsonResponse({"message":"coupon code exist on this product"})          
               else :
                     return JsonResponse({"message":"coupon code expired"})
        else:
           return  JsonResponse({"response":"no cookie present"}) 





class CheckoutView(LoginRequiredMixin,View):
     CART_ID="CART_ID"
     def get(self,request):
            cart=request.COOKIES.get(self.CART_ID)
            if cart:
                 user=request.user
                 if Cart.objects.filter(pk=cart).exists():
                       cart_obj=Cart.objects.get(pk=cart)
                       cart_items=cart_obj.cartitem_set.all()
                       context={"siteuser":user,"cart_items":cart_items}
                       print context
                       return render(request,"checkout.html",context)
                 else:   
                       messages.error(self.request, 'no cart')
                       response =  redirect(reverse("home"))
                       response.delete_cookie(CART_ID)
                       return response                               
            else:
                #disable checkout button
                messages.error(self.request, 'nothing in cart')
                return  redirect(reverse("home"))


class PlaceOrder(LoginRequiredMixin,FormView):
     template_name="place-order.html"
     form_class=PlaceOrderForm
     #paytm redirect url
     success_url="user/orders/"
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
              if cart.objects.filter(pk=cart).exists():
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
              else:
                 messages.error(self.request, 'no cart')
                 response = redirect(reverse("home"))
                 response.delete_cookie(CART_ID)
                 return response           
              return super(PlaceOrder, self).form_valid(form)
           else:
                messages.error(self.request, 'nothing in cart')
                return redirect(reverse("home")) 

#callbackview
class OrderProcessCompleted(View):
     def post(self,request):
       CART_ID="CART_ID"
       cart=request.COOKIES.get(CART_ID)
       if cart:
         cart_obj=Cart.objects.get(pk=cart)
         for cart_product in cart_obj.cartitem_set.all():
            if cart_product.coupon_code:
              CustomerCouponUsedTrack.objects.create(customer=request.user,coupon_code=cart_product.coupon_code)
         cart_obj=Cart.objects.filter(pk=cart).delete()
         messages.success(self.request,'order placed buddy')
         # paytm crdentials and redirection
         response = redirect(reverse("user-orders"))
         response.delete_cookie(CART_ID)
         return response
       else:
         return Http404



class CancelOrder(LoginRequiredMixin,View):
   """take ajax calls to cancel order with 
        order_id and order_product_id as parameter in post request"""
   def post(self,request):
        order=request.POST.get("order_id")
        order_obj=get_object_or_404(Order,pk=order)
        if (request.user==order_obj.Order_Customer.customer.User_customer):
             order_items_id=request.POST.getlist("order_product_id")
             for product_id in order_items_id:
                  order_product=get_object_or_404(Order_Product_Specs,pk=product_id)
                  if order_product.Order_Status.status_for_order=="DELIVERED":
                     messages.error(self.request, 'order delivered')
                     return redirect(reverse("user-orders"))
                  else:
                     order_product.Order_Status=Order_Status_Model.objects.get(status_for_order="CANCELLED")
                     order_product.save()
        else:
            return  HttpResponse(status=401)   
        return redirect(reverse("user-orders"))
   

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
         return render(request, 'admin-catalog-basecategory.html', {'contacts':contacts})



class AdminBasecategoryCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
   model = BaseCategory
   fields = ["Base_Category","Base_Category_Pic"]
   template_name="base-category-edit.html"
   success_url="/adminsite/catalog/basecategories/"
   def test_func(self):
           return self.request.user.is_superuser

class AdminBasecategoryUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
   model = BaseCategory
   fields = ["Base_Category","Base_Category_Pic"]
   template_name="base-category-edit.html"
   success_url="/adminsite/catalog/basecategories/"
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
         return render(request, 'admin-catalog-subcategory.html', {'contacts':contacts})
   
class AdminSubcategoryCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
   """admin sub category form handling"""
   model=SubCategory
   template_name="sub-category-edit.html"
   success_url="/adminsite/catalog/subcategories/"
   fields=["Base_category_Key","Sub_Category","Sub_Category_Pic"]
   def test_func(self):
           return self.request.user.is_superuser
  
class AdminSubcategoryUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
   """admin sub category form handling"""
   model=SubCategory
   template_name="sub-category-edit.html"
   fields=["Base_category_Key","Sub_Category","Sub_Category_Pic"]
   success_url="/adminsite/catalog/subcategories/"
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
         return render(request,"admin-order.html",{"contact":contacts,"status":status,'filter': filter}) 

class OrderStatusChange(LoginRequiredMixin,UserPassesTestMixin,View):
  """ use  order_product_id and order_id """
  def test_func(self):
        return self.request.user.is_superuser
  def post(self,request):
       order_id=request.POST.get("order_id")
       if Order.objects.filter(pk=order_id).exists():
          order=Order.objects.get(pk=order_id)
          product_id=request.POST.get("order_product_id")
          ordered_product=Order_Product_Specs.objects.get(pk=product_id)
          ordered_product.Order_Status=Order_Status_Model.objects.get(status_for_order=request.POST.get("status")),
          return JsonResponse({"message":"status changed"+"to"+request.POST.get["status"]})
       else:
          return JsonResponse({"message":"order does not exist"})

#sales panel stuff----------------------------------------------->
class SalesSignin(FormView):
    """sales login form and validation"""
    template_name="sales-login.html"
    form_class=SignInForm
    success_url="siteuser/user"
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
      return render(request,"sales-panel.html",{"sales":sales,"coupon_used_list":coupon_used_list}) 


class SalesSignOut(LoginRequiredMixin,View):
    def get(self,request):
          logout(request)
          return redirect(reverse("sales-signin"))

#seller stuff--------------------------> 
class SellerPanel(LoginRequiredMixin,UserPassesTestMixin,View):
  """sales panel"""
  def test_func(self):
      return Seller.objects.filter(seller_user=self.request.user).exists()
  def get(self,request):
      """seller panel landing page"""
      seller=Seller.objects.get(seller_user=request.user)
      return render(request,"seller-panel.html",{"seller":seller})

class SellerSignin(FormView):
    """sales login form and validation"""
    template_name="seller-login.html"
    form_class=SignInForm
    success_url="sellersite/panel"
    def form_valid(self,form):
           user=authenticate(self.request,username=form.cleaned_data["username"],password=form.cleaned_data["password"])
           if Seller.objects.filter(seller_user__username=form.cleaned_data["username"]).exists():
               if user is not None:
                     if user.is_active:
                         login(self.request,user)
                         return super(SellerSignin, self).form_valid(form)
                     else:
                           messages.error(self.request, 'Invalid username or password')
                           return redirect(reverse("seller-signin"))    
               else:
                   messages.error(self.request, 'Invalid username or password')
                   return redirect(reverse("seller-signin"))
           else:
               messages.error(self.request, 'Invalid username or password')
               return redirect(reverse("seller-signin"))

class SellerSignOut(LoginRequiredMixin,View):
    def get(self,request):
          logout(request)
          return redirect(reverse("seller-signin"))

class SellerProductAdd(LoginRequiredMixin,CreateView,UserPassesTestMixin):
   model=Product
   template_name="seller-product-cu.html"
   fields="__all__"
   success_url="sellersite/panel"
   def test_func(self):
      return Seller.objects.filter(seller_user=self.request.user).exists()

class SellerProductUpdate(LoginRequiredMixin,UpdateView,UserPassesTestMixin):
   model=Product
   fields="__all__"
   template_name="seller-product-cu.html"
   success_url="sellersite/panel"
   def test_func(self):
      return Seller.objects.filter(seller_user=self.request.user).exists()

class SellerProductDelete(LoginRequiredMixin,DeleteView,UserPassesTestMixin):
   model=Product
   success_url="sellersite/panel"
   def test_func(self):
      return Seller.objects.filter(seller_user=self.request.user).exists()
















