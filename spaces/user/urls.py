from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.user_register_view, name='register'),
    path('login/', views.user_login_view, name='login'),
    path('profile/', views.user_profile_view, name='profile'),
    path('logout/', views.user_logout_view, name='logout'),
    path('user_search/', views.user_search, name='search'),

    path('add/<int:user_id>', views.add_user, name='add_user'),
    path('remove/<int:user_id>', views.remove_user, name='remove_user'),
]