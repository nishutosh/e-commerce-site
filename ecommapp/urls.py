from django.conf.urls import url,include
from .views import HomeView

urlpatterns = [
    url(r'^home/',HomeView.as_view()),
]


