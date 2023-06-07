from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
# Create your views here.
from django.http import HttpResponseRedirect
from frontend.decorators import unauthenticated_user
import requests

from ssudms import settings


def landingpage(request):
    context = {

    }
    return render(request, 'landingpage/index.html', context)


@unauthenticated_user
@require_http_methods(['GET', 'POST'])
def login_page(request):
    try:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('login[password]')
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('frontend-index-page')
            else:
                messages.error(request, 'Username or password is incorrect.')
                return render(request, 'landingpage/login.html')
        return render(request, 'landingpage/login.html')
    except Exception as e:
        print(e)


def get_logout_url(request):
    keycloak_redirect_url = settings.OIDC_OP_LOGOUT_ENDPOINT or None
    return keycloak_redirect_url + "?redirect_uri=" + request.build_absolute_uri(settings.LOGOUT_REDIRECT_URL)


def logout_page(request):
    django_logout_url = settings.LOGOUT_REDIRECT_URL or '/'
    
    logout_url = get_logout_url(request)
    logout(request)
    return HttpResponseRedirect(logout_url)
