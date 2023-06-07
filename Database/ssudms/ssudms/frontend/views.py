from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from . decorators import unauthenticated_user
from . forms import LoginForm


def indexPage(request):
    try:
        return render(request, 'frontend/index.html')
    except Exception as e:
        print(e)


@unauthenticated_user
@require_http_methods(['GET', 'POST'])
def loginPage(request):
    try:
        form = LoginForm()

        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    next_url = request.GET.get('next')
                    return redirect('/') if next_url is None else redirect(next)
                else:
                    messages.error(request, 'Incorrect username/password.')
                    context = {
                        'form': form

                    }
                    return render(request, 'frontend/login.html', context)

            messages.error(request, 'Incorrect username/password.')
            context = {
                'form': form
                }
            return render(request, 'frontend/login.html', )

        context = {
            'form': form
        }
        return render(request, 'frontend/login.html', context)

    except Exception as e:
        request.session['error404'] = 1
        return redirect('/404')


def logoutPage(request):
    logout(request)
    return redirect('/')




