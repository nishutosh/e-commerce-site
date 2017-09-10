from django.conf.urls import url,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$',HomeView.as_view(),name="home"),
    url(r'(?P<basefield>[\w-]+)/(?P<subfield>[\w-]+)/$',ProductList.as_view()),
    url(r'(?P<basefield>[\w-]+)/(?P<subfield>[\w-]+)/(?P<pk>\w+)$',ProductDetails.as_view()),
    url(r'register/$',RegisterView.as_view(),name="register"),
    url(r'signin/$',SignInView.as_view(),name="signin"),
    url(r'signout/$',SignOutView.as_view(),name="signout"),
    url(r'user-dashboard/$',UserDashboard.as_view(),name="user-dashboard"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
