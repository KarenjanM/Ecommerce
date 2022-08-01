from django.urls import path
from .views import new_login, new_logout, register

urlpatterns = [
    path('login/', new_login, name='login'),
    path('logout/', new_logout, name='logout'),
    path('register/', register, name='register')
]