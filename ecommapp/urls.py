from django.conf.urls import url,include
from .views import HomeView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^home/',HomeView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


