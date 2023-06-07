from django.conf.urls import url
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.indexPage, name='frontend-index-page'),
    path('login/', views.loginPage, name='frontend-login-page'),
    path('logout/', views.logoutPage, name='frontend-logout-page'),
]
