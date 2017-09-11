from django.conf.urls import url,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

userurls=[
   url(r'edit-info',EditFormView.as_view(),name="edit-form"),
   url(r'security',SecurityView.as_view(),name="security"),
]

urlpatterns = [
    url(r'home/',HomeView.as_view(),name="home"),
    url(r'(?P<basefield>[\w-]+)/(?P<subfield>[\w-]+)/$',ProductList.as_view()),
    url(r'(?P<basefield>[\w-]+)/(?P<subfield>[\w-]+)/(?P<pk>\w+)$',ProductDetails.as_view()),
    url(r'register/$',RegisterView.as_view(),name="register"),
    url(r'signin/$',SignInView.as_view(),name="signin"),
    url(r'signout/$',SignOutView.as_view(),name="signout"),
    url(r'cart/$',PostGetCartView.as_view(),name="cart"),
    url(r'cart/delete$',DeleteCartView.as_view(),name="cartdelete"),
    url(r'cart/checkout/$',CheckoutView.as_view(),name="checkout"),
    url(r'user-dashboard/$',UserDashboard.as_view(),name="user-dashboard"),
    url(r'user/',include(userurls))
    # url(r'payment/$)',PaymentView.as_view(),name="payment"),
    # url(r'order/$',OrderProduct.as_view(),name="payment")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
