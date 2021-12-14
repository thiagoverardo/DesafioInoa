from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path('contact/', views.ContactView.as_view(), name="contact"),
    path('success/', views.ContactSuccessView.as_view(), name="success"),
]