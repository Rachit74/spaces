from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.user_register_view, name='register'),
    path('login/', views.user_login_view, name='login'),
]