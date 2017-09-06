from django.conf.urls import url,include
from .views import HomeView,ProductList,ProductDetails
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'home/',HomeView.as_view()),
    url(r'(?P<basefield>[\w-]+)/(?P<subfield>[\w-]+)$',ProductList.as_view()),
    url(r'(?P<basefield>[\w-]+)/(?P<subfield>[\w-]+)/(?P<code>\w+)/$',ProductDetails.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
