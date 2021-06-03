from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register_user),
    path('login', views.login_user),
    path('logout', views.logout),
    path('success', views.success)

]