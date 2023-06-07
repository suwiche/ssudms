from django.urls import path

from . views import landingpage, login_page, logout_page
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

urlpatterns = [
    path('', landingpage, name='landingpage-index-page'),
    path('login/', login_page, name='landingpage-login-page'),
    path('logout/', logout_page, name='landingpage-logout-page'),
]