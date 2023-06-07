from django.shortcuts import render

@login_required(login_url='/login')
@require_http_methods(['GET', 'POST'])