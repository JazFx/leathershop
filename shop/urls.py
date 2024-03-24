from django.contrib import admin
from django.urls import path, include
from core import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='infoproduct'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.profile_view, name='profile'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:pk>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.submit_order, name='checkout'),
    path('submit_order/', views.submit_order, name='submit_order'),
    path('user/reg/', views.reg, name='registration'),
    path('user/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/profile/', views.profile_redirect, name='profile_redirect'),
]
