from django.urls import path

from . views import landingpage, login_page, logout_page, signup_page
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

urlpatterns = [
    path('', landingpage, name='landingpage-index-page'),
    path('login/', login_page, name='landingpage-login-page'),
    path('signup/', signup_page, name='landingpage-signup-page'),
    path('logout/', logout_page, name='landingpage-logout-page'),
]