from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@login_required(login_url='/login')
@require_http_methods(['GET', 'POST'])
def dashboardIndexPage(request):
    try:
        group = str(request.user.groups.all()[0])

        if str(group) == "admin":
            context = {
                'here': 'here'
            }
            return render(request, 'dashboard/dashboard.html', context)
    except Exception as e:
        print(e)
