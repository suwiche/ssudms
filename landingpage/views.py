from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages
# Create your views here.
from django.http import HttpResponseRedirect
from frontend.decorators import unauthenticated_user
from django.contrib import messages
from backend.forms import SignUpForm
import requests

from ssudms import settings


def landingpage(request):
    context = {

    }
    return render(request, 'landingpage/index.html', context)


def signup_page(request, action=None):
    try:
        if action is None:
            if request.method == "POST":
                with transaction.atomic():
                    form = SignUpForm(request.POST)
                    if form.is_valid():
                        username = form.cleaned_data['username']
                        first_name = form.cleaned_data['first_name']
                        last_name = form.cleaned_data['last_name']
                        email = form.cleaned_data['email']
                        password = form.clean_password()
                        group = form.cleaned_data['group']                        
                        user = User.objects.create_user(username=username, email=email, first_name=first_name,
                                                        last_name=last_name,
                                                        password=password, is_active=0,is_superuser=0,is_staff=1)
                        user.save()
                        user.groups.add(group)

                        return JsonResponse({'statusMsg': 'Success!'}, status=200)
                    else:
                        errors = []
                        for field in form:
                            for error in field.errors:
                                errors.append(error)
                        return JsonResponse({'statusMsg': 'Form is invalid!', 'errors': errors}, status=404)

            elif request.method == "GET":
                context = {
                    'action': 'users',
                    'module_name': 'Users',
                    'breadcrumbs': ['Backend', 'Users'],
                    'title': 'Backend - Users',
                    'data': User.objects.all(),
                    'form': SignUpForm()
                }
                return render(request, 'landingpage/signup.html', context)
    except Exception as e:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            error = ''
            for row in e:
                error = row
            return JsonResponse({'statusMsg': 'error', 'error': error}, status=404)

        messages.success(request, str(e))
        return redirect('landingpage-signup-page')


@unauthenticated_user
@require_http_methods(['GET', 'POST'])
def login_page(request):
    try:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('login[password]')
            user = authenticate(request, username=username, password=password)
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
    
    logout_url = django_logout_url
    logout(request)
    return HttpResponseRedirect(logout_url)
