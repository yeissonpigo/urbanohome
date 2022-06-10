from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/success', views.register_success, name='register_success'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('items/', views.show_items, name='items'),
    path('card/', views.card, name='card'),
    path('cart/', views.card_index, name='card_index'),
    path('delete_cart/', views.delete_cart, name='delete_card'),
    path('checkout/', views.checkout, name='checkout'),
    #path('finishpurchase/', views.finish_purchase, name='finishpurchase'),
    path('cancelpurchase/', views.delete_venta, name='cancelpurchase'),
    path('', views.index, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('pay_response/', views.pay_response, name='pay_response'),
    path('pay_confirmation/', views.pay_confirmation, name='pay_confirmation'),
    path('profile/', views.profile, name='profile'),
    path('products/', views.products, name='products'),
]