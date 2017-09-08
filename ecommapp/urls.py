from django.conf.urls import url,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    url(r'home/',HomeView.as_view()),
    url(r'(?P<basefield>[\w-]+)/(?P<subfield>[\w-]+)$',ProductList.as_view()),
    url(r'(?P<basefield>[\w-]+)/(?P<subfield>[\w-]+)/(?P<pk>\w+)/$',ProductDetails.as_view()),
    url(r'register/$',RegisterView.as_view()),
    url(r'account-created/$',TemplateView.as_view(template_name="registration_success.html")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
