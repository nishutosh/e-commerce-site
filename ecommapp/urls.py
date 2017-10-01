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
   url(r'reviews/$',UserReviewList.as_view(),name="user-reviews"),
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
]

commonurls=[
    url(r'^$',HomeView.as_view(),name="home"),
    url(r'product/(?P<basefield>[\w-]+)/(?P<subfield>[\w-]+)/$',ProductList.as_view()),
    url(r'product/(?P<basefield>[\w-]+)/(?P<subfield>[\w-]+)/(?P<pk>\w+)$',ProductDetails.as_view()),
]

orderurls=[
url(r'place-order/$',PlaceOrder.as_view(),name="place-order"),
url(r'cancel-order/$',CancelOrder.as_view(),name="cancel-order"),

]

adminurls=[
   url(r'signin/$',AdminSignin.as_view(),name="admin-login"),
   url(r'^$',AdminPanel.as_view(),name="admin-panel"),
   url(r'signout/$',AdminSignOut.as_view(),name="admin-signout"),
   url(r'catalog/basecategories/$',AdminBaseCategory.as_view(),name="admin-catalog-base"),
   url(r'catalog/edit-basecategories/(?P<bcat_id>[\w-]+)$',AdminBasecategoryFormView.as_view(),name="admin-catalog-base-edit"),
   url(r'catalog/edit-basecategories/delete/$',AdminBasecategoryDeleteView.as_view(),name="admin-catalog-base-delete"),
   url(r'catalog/subcategories/$',AdminSubCategory.as_view(),name="admin-catalog-sub"),
   url(r'catalog/edit-subcategories/(?P<scat_id>[\w-]+)$',AdminSubcategoryFormView.as_view(),name="admin-catalog-sub-edit"),
   url(r'catalog/edit-subcategories/delete/$',AdminSubcategoryDeleteView.as_view(),name="admin-catalog-sub-delete"),
   url(r'catalog/products/$',AdminProduct.as_view(),name="admin-products"),
   url(r'catalog/edit-products/(?P<p_id>[\w-]+)$',AdminProductFormView.as_view(),name="admin-catalog-base-edit"),

]

urlpatterns = [
    url(r'^',include(commonurls)),
    url(r'^',include(authurls)),
    url(r'cart/',include(carturls)),
    url(r'user/',include(userurls)),
    url(r'order/',include(orderurls)),
    url(r'admin-panel/',include(adminurls))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
