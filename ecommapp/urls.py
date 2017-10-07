from django.conf.urls import url,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

userurls=[
   url(r'edit-info/$',EditFormView.as_view(),name="edit-form"),
   url(r'security/$',SecurityView.as_view(),name="security"),
   url(r'credits/$',FashVoltsCreditView.as_view(),name="credits"),
   url(r'coupoun-applied/$',CoupounAppliedView.as_view(),name="coupouns"),
   url(r'reviews/$',UserReviewList.as_view(),name="user-reviews"),
   url(r'orders/$',UserOrderList.as_view(),name="user-orders"),
   url(r'user-dashboard/$',UserDashboard.as_view(),name="user-dashboard"),
]
carturls=[
    url(r'cartitems/$',PostGetCartView.as_view(),name="cart"),
    url(r'delete/$',DeleteCartView.as_view(),name="cartdelete"),
    url(r'checkout/$',CheckoutView.as_view(),name="checkout"),
    url(r'apply-coupon/$',ApplyCoupon.as_view(),name="apply-code"),
]
authurls=[
    url(r'register/$',RegisterView.as_view(),name="register"),
    url(r'signin/$',SignInView.as_view(),name="signin"),
    url(r'signout/$',SignOutView.as_view(),name="signout"),
    url(r'validate/$',UserNameCheckView.as_view(),name="check"),
]
commonurls=[
    url(r'(?P<basefield>[\w-]+)/(?P<subfield>[\w-]+)/$',ProductList.as_view()),
    url(r'(?P<basefield>[\w-]+)/(?P<subfield>[\w-]+)/(?P<pk>\w+)$',ProductDetails.as_view()),
    url(r'',HomeView.as_view(),name="home"),
]
orderurls=[
    url(r'place-order/$',PlaceOrder.as_view(),name="place-order"),
    url(r'cancel-order/$',CancelOrder.as_view(),name="cancel-order"),
]
adminurls=[
   url(r'signin/$',AdminSignin.as_view(),name="admin-login"),
   url(r'panel/$',AdminPanel.as_view(),name="admin-panel"),
   url(r'signout/$',AdminSignOut.as_view(),name="admin-signout"),
   url(r'catalog/basecategories/$',AdminBaseCategory.as_view(),name="admin-catalog-base"),
   url(r'catalog/create-basecategories/$',AdminBasecategoryCreateView.as_view(),name="admin-catalog-base-new"),
   url(r'catalog/edit-basecategories/(?P<pk>[0-9]+)$',AdminBasecategoryUpdateView.as_view(),name="admin-catalog-base-edit"),
   url(r'catalog/edit-basecategories/delete/$',AdminBasecategoryDeleteView.as_view(),name="admin-catalog-base-delete"),
   url(r'catalog/subcategories/$',AdminSubCategory.as_view(),name="admin-catalog-sub"),
   url(r'catalog/create-subcategories/$',AdminSubcategoryCreateView.as_view(),name="admin-catalog-sub-new"),
   url(r'catalog/edit-subcategories/(?P<pk>[0-9]+)$',AdminSubcategoryUpdateView.as_view(),name="admin-catalog-sub-edit"),
   url(r'catalog/edit-subcategories/delete/$',AdminSubcategoryDeleteView.as_view(),name="admin-catalog-sub-delete"),
   url(r'admin-order/$',AdminOrderView.as_view(),name="admin-order"),

]
urlpatterns = [
    url(r'home/',include(commonurls)),
    url(r'auth/',include(authurls)),   
    url(r'cart/',include(carturls)),
    url(r'user/',include(userurls)),
    url(r'order/',include(orderurls)),
    url(r'adminsite/',include(adminurls)),
    url(r'search/',ElasticSearch,name="search")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
