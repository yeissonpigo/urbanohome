from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/success', views.register_success, name='register_success'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('items/', views.show_items, name='items'),
    path('card/', views.card, name='card'),
    path('cart/', views.card_index, name='card_index')
]