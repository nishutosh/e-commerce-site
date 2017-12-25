from django.conf.urls import url,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

userurls=[
   url(r'user-dashboard/$',UserDashboard.as_view(),name="user-dashboard"),
   url(r'edit-info/$',EditFormView.as_view(),name="edit-form"),
   url(r'security/$',SecurityView.as_view(),name="security"),
   url(r'credits/$',FashVoltsCreditView.as_view(),name="credits"),
   url(r'coupon-applied/$',CoupounAppliedView.as_view(),name="coupons"),
 #  url(r'reviews/$',UserReviewList.as_view(),name="user-reviews"),
   url(r'orders/$',UserOrderList.as_view(),name="user-orders")
]

authurls=[
    url(r'register/$',RegisterView.as_view(),name="register"),
    url(r'signin/$',SignInView.as_view(),name="signin"),
    url(r'signout/$',SignOutView.as_view(),name="signout"),

]

carturls=[
    url(r'^$',PostGetCartView.as_view(),name="cart"),
    url(r'delete/$',DeleteCartView.as_view(),name="cartdelete"),
    url(r'checkout/$',CheckoutView.as_view(),name="checkout"),
    url(r'apply-coupon/$',ApplyCoupon.as_view(),name="apply-coupon"),
    url(r'apply-credit/$',creditapply,name="apply-credit"),
    url(r'remove-credit/$',removeapply,name="remove-credit"),
]
wishlisturls=[
  url(r'product/$',GetPostToWishlist.as_view(),name="wishlist"),
  url(r'product-count/$',GetToWishListCount,name="wishlist-count"),
  url(r'delete/$',DeleteFromWishList.as_view(),name="delete-wishlist"),

]

commonurls=[
    url(r'^$',HomeView.as_view(),name="home"),
    url(r'product/(?P<basefield>[\w-]+)/(?P<subfield>[\w-]+)/$',ProductList.as_view()),
    url(r'product/(?P<basefield>[\w-]+)/(?P<subfield>[\w-]+)/(?P<pk>\w+)$',ProductDetails.as_view()),
]

orderurls=[
url(r'place-order/$',PlaceOrder.as_view(),name="place-order"),
url(r'cancel-order/$',CancelOrder.as_view(),name="cancel-order"),
url(r'order-payment/(?P<order_id>\d+)/$',OrderPayment.as_view(),name="order-payment"),
]

adminurls=[
   url(r'signin/$',AdminSignin.as_view(),name="admin-login"),
   url(r'^$',AdminPanel.as_view(),name="admin-panel"),
   url(r'signout/$',AdminSignOut.as_view(),name="admin-signout"),
   url(r'catalog/basecategories/$',AdminBaseCategory.as_view(),name="admin-catalog-base"),
   url(r'catalog/create-basecategories/$',AdminBasecategoryCreateView.as_view(),name="admin-catalog-base-new"),
   url(r'catalog/edit-basecategories/(?P<pk>[0-9]+)$',AdminBasecategoryUpdateView.as_view(),name="admin-catalog-base-edit"),
   url(r'catalog/edit-basecategories/delete/$',AdminBasecategoryDeleteView.as_view(),name="admin-catalog-base-delete"),
   url(r'catalog/subcategories/$',AdminSubCategory.as_view(),name="admin-catalog-sub"),
   url(r'catalog/create-subcategories/$',AdminSubcategoryCreateView.as_view(),name="admin-catalog-sub-new"),
   url(r'catalog/edit-subcategories/(?P<pk>[0-9]+)$',AdminSubcategoryUpdateView.as_view(),name="admin-catalog-sub-edit"),
   url(r'catalog/edit-subcategories/delete/$',AdminSubcategoryDeleteView.as_view(),name="admin-catalog-sub-delete"),
   url(r'catalog/products/$',AdminProduct.as_view(),name="admin-catalog-product"),
   url(r'catalog/edit-products/$',AdminProductCreateView.as_view(),name="admin-catalog-product-new"),
   url(r'catalog/edit-products/(?P<pk>[\w-]+)$',AdminProductUpdateView.as_view(),name="admin-catalog-product-edit"),
   url(r'catalog/edit-products/delete/$',AdminProductDeleteView.as_view(),name="admin-catalog-product-delete"),
   url(r'catalog/products-pics/$',AdminProductPics.as_view(),name="admin-catalog-product-pics"),
   url(r'catalog/edit-products-pics/$',AdminProductPicsCreateView.as_view(),name="admin-catalog-product-pics-new"),
   url(r'catalog/edit-products-pics/(?P<pk>[\w-]+)$',AdminProductPicsUpdateView.as_view(),name="admin-catalog-product-pics-edit"),
   url(r'catalog/edit-products-pics/delete/$',AdminProductPicsDeleteView.as_view(),name="admin-catalog-product-pics-delete"),
   url(r'customer/sellers/$',AdminSellers.as_view(),name="admin-customer-sellers"),
   url(r'customer/edit-sellers/$',AdminSellersCreateView.as_view(),name="admin-customer-sellers-new"),
   url(r'customer/edit-sellers/(?P<pk>[\w-]+)$',AdminSellersUpdateView.as_view(),name="admin-customer-sellers-edit"),
   url(r'customer/edit-sellers/delete/$',AdminSellersDeleteView.as_view(),name="admin-customer-sellers-delete"),
   url(r'customer/enduser/$',AdminCustomer.as_view(),name="admin-customer-enduser"),
   url(r'marketing/coupon/$',AdminCoupon.as_view(),name="admin-marketing-coupon"),
   url(r'marketing/edit-coupon/$',AdminCouponCreateView.as_view(),name="admin-marketing-coupon-new"),
   url(r'marketing/edit-coupon/(?P<pk>[\w-]+)$',AdminCouponUpdateView.as_view(),name="admin-marketing-coupon-edit"),
   url(r'marketing/edit-coupon/delete/$',AdminCouponDeleteView.as_view(),name="admin-marketing-coupon-delete"),
   url(r'admin-order/$',AdminOrderView.as_view(),name="admin-order"),
   url(r'admin-order/order-list-by-category$',AdminOrderViewByCategory.as_view(),name="admin-order-by-category"),
   url(r'admin-order/order-list-by-category/(?P<subfield>[\w-]+)$',AdminOrderViewByGivenCategory.as_view(),name="admin-order-by-given-category"),
   url(r'admin-order/change-product-status$',OrderProductStatusChange.as_view(),name="admin-order-product-status"),
   url(r'admin-order/change-order-status$',WholeOrderPaymentConfirm.as_view(),name="admin-order-status"),
   url(r'admin-reports/total-order$',AdminReportsOrderView.as_view(),name="admin-reports-orders"),
   url(r'admin-reports/get-order-stats$',OrderReportApi.as_view(),name="admin-reports-orders-stats"),
   url(r'admin-reports/total-users$',AdminReportsUserView.as_view(),name="admin-reports-users"),
   url(r'admin-reports/get-user-stats$',UserReportApi.as_view(),name="admin-reports-users-stats")

]

salesurls=[
 url(r'signin/$',SalesSignin.as_view(),name="sales-signin"),
 url(r'^$',SalesPanel.as_view(),name="sales-panel"),
 url(r'signout/$',SalesSignOut.as_view(),name="sales-signout"),

]

customurls=[

 url(r'^$',CustomView.as_view(),name="sales-panel"),


]
custommoduleurls=[
 url(r'brand/(?P<type>[\w-]+)$',CustomModule.as_view(),name="custom-home"),
 url(r'edit/(?P<pk>[\w]+)$',CustomeModuleMain.as_view(),name="edit-pic"),
 url(r'phone/(?P<brand_slug>[\w-]+)$',getphones,name="get-phones"),
 url(r'submit$',PostCustomModule.as_view(),name="submit-custom-image"),
 url(r'submit-images$',PostCustomModulePics.as_view(),name="submit-custom-working-images"),


]

urlpatterns = [
    url(r'cart/',include(carturls)),
    url(r'user/',include(userurls)),
    url(r'order/',include(orderurls)),
    url(r'search/',ElasticSearch,name="search"),
    url(r'admin-panel/',include(adminurls)),
    url(r'sales-panel/',include(salesurls)),
    url(r'custom/',include(customurls)),
    url(r'custom-module/',include(custommoduleurls)),
    url(r'wishlist/',include(wishlisturls)),
    url(r'^',include(commonurls)),
    url(r'^',include(authurls)),
  
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
