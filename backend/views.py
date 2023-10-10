from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, ExtensionForm, TypeForm, ProcessForm, ServicesForm, StatusForm, LevelForm, \
    UpdateUserForm, DetailsAttributeForm, WorkerAttributeForm, TransactionAttributeForm, Form
from .models import LibraryExtensions, LibraryTypes, LibraryProcess, LibraryServices, LibraryStatus, LibraryLevel, \
    DetailsAttribute, LibraryCitymun, LibraryBarangay, WorkerAttribute, Forms
from .decorators import allowed_users
import datetime


@login_required(login_url='/login')
def index_page(request):
    try:
        context = {
            'action': 'admin',
            'title': 'Admin'
        }
        print('here')
        return render(request, 'backend/index.html', context)
    except Exception as e:
        print(e)


@login_required(login_url='/login')
def users_page(request, action=None, pk=None):
    try:
        if action is None and pk is None:
            if request.method == "POST":
                with transaction.atomic():
                    form = SignUpForm(request.POST)
                    if form.is_valid():
                        username = form.cleaned_data['username']
                        first_name = form.cleaned_data['first_name']
                        last_name = form.cleaned_data['last_name']
                        email = form.cleaned_data['email']
                        password = form.clean_password()
                        is_active = form.cleaned_data['is_active']
                        is_superuser = form.cleaned_data['is_superuser']
                        is_staff = form.cleaned_data['is_staff']
                        group = form.cleaned_data['group']

                        user = User.objects.create_user(username=username, email=email, first_name=first_name,
                                                        last_name=last_name,
                                                        password=password, is_active=1 if is_active is True else 0,
                                                        is_superuser=1 if is_superuser is True else 0,
                                                        is_staff=1 if is_staff is True else 0)
                        user.save()
                        print(group)
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
                return render(request, 'backend/users.html', context)

        if action is not None and pk is not None:
            user = User.objects.get(id=pk)
            if action == "update":
                if request.method == "GET":
                    context = {
                        'action': 'update_user',
                        'module_name': 'Users',
                        'breadcrumbs': ['Backend', 'Users'],
                        'title': 'Backend - Update User',
                        'form': UpdateUserForm(instance=user, initial={'group': user.groups.all()[0]}),
                        'data': user,
                    }
                    return render(request, 'backend/users.html', context)

                elif request.method == "POST":
                    form = UpdateUserForm(request.POST, instance=user)

                    if form.is_valid():
                        group = form.cleaned_data['group']
                        user_group = user.groups.all()[0]
                        form = form.save()
                        if group is not None:
                            form.groups.add(group)
                        elif group is None:
                            user.groups.add(user_group)
                        return JsonResponse({'statusMsg': 'Success'}, status=200)

                    return JsonResponse({'statusMsg': 'Invalid!'}, status=404)
    except Exception as e:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            error = ''
            for row in e:
                error = row
            return JsonResponse({'statusMsg': 'error', 'error': error}, status=404)

        messages.success(request, str(e))
        return redirect('backend-users-page')


@login_required(login_url='/login')
def extensions_page(request, action=None, pk=None):
    try:
        if action is None and pk is None:
            if request.method == "POST":
                form = ExtensionForm(request.POST)
                if form.is_valid():
                    name = form.clean_extension()
                    s = form.cleaned_data['status']
                    extension = LibraryExtensions.objects.create(name=name, status=s, created_by=request.user)
                    extension.save()

                    return JsonResponse({'statusMsg': 'Success!'}, status=200)
                else:
                    return JsonResponse({'statusMsg': 'Form is invalid!'}, status=404)
            elif request.method == "GET":
                context = {
                    'action': 'extensions',
                    'module_name': 'Extensions',
                    'breadcrumbs': ['Backend', 'Extensions'],
                    'title': 'Backend - Extensions',
                    'data': LibraryExtensions.objects.all(),
                    'form': ExtensionForm()
                }
                return render(request, 'backend/extensions.html', context)

        elif action is not None and pk is not None:
            extension = LibraryExtensions.objects.get(id=pk)
            if action == "update":
                if request.method == "GET":
                    context = {
                        'action': 'update_extension',
                        'module_name': 'Extensions',
                        'breadcrumbs': ['Backend', 'Extensions'],
                        'title': 'Backend - Update Extension',
                        'form': ExtensionForm(instance=extension),
                        'data': extension
                    }
                    return render(request, 'backend/extensions.html', context)

                elif request.method == "POST":
                    form = ExtensionForm(request.POST, instance=extension)

                    if form.is_valid():
                        update_form = form.save()
                        update_form.date_updated = datetime.datetime.now()
                        update_form.updated_by = request.user
                        update_form.save()
                        return JsonResponse({'statusMsg': 'Success'}, status=200)

                    return JsonResponse({'statusMsg': 'Invalid!'}, status=404)
    except Exception as e:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            error = ''
            for row in e:
                error = row
            return JsonResponse({'statusMsg': 'error', 'error': error}, status=404)

        messages.success(request, str(e))
        return redirect('backend-extensions-page')


@login_required(login_url='/login')
def process_page(request, action=None, pk=None):
    try:
        if action is None and pk is None:
            if request.method == "POST":
                form = ProcessForm(request.POST)
                if form.is_valid():
                    name = form.clean_process()
                    s = form.cleaned_data['status']
                    process = LibraryProcess.objects.create(name=name, status=s, created_by=request.user)
                    process.save()

                    return JsonResponse({'statusMsg': 'Success!'}, status=200)
                else:
                    return JsonResponse({'statusMsg': 'Form is invalid!'}, status=404)

            if request.method == "GET":
                context = {
                    'action': 'process',
                    'module_name': 'Process',
                    'breadcrumbs': ['Backend', 'Process'],
                    'title': 'Backend - Process',
                    'data': LibraryProcess.objects.all(),
                    'form': ProcessForm()
                }
                return render(request, 'backend/process.html', context)

        elif action is not None and pk is not None:
            process = LibraryProcess.objects.get(id=pk)
            if action == "update":
                if request.method == "GET":
                    context = {
                        'action': 'update_process',
                        'module_name': 'Process',
                        'breadcrumbs': ['Backend', 'Process'],
                        'title': 'Backend - Update Process',
                        'form': ProcessForm(instance=process),
                        'data': process
                    }
                    return render(request, 'backend/process.html', context)

                elif request.method == "POST":
                    form = ProcessForm(request.POST, instance=process)
                    if form.is_valid():
                        update_form = form.save()
                        update_form.date_updated = datetime.datetime.now()
                        update_form.updated_by = request.user
                        update_form.save()
                        return JsonResponse({'statusMsg': 'Success'}, status=200)

                    return JsonResponse({'statusMsg': 'Invalid!'}, status=404)
    except Exception as e:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            error = ''
            for row in e:
                error = row
            return JsonResponse({'statusMsg': 'error', 'error': error}, status=404)

        messages.success(request, str(e))
        return redirect('backend-process-page')


@login_required(login_url='/login')
def services_page(request, action=None, pk=None):
    try:
        if action is None and pk is None:
            if request.method == "POST":
                form = ServicesForm(request.POST)
                if form.is_valid():
                    name = form.clean_service()
                    s = form.cleaned_data['status']
                    services = LibraryServices.objects.create(name=name, status=s, created_by=request.user)
                    services.save()

                    return JsonResponse({'statusMsg': 'Success!'}, status=200)
                else:
                    return JsonResponse({'statusMsg': 'Form is invalid!'}, status=404)
            elif request.method == "GET":
                context = {
                    'action': 'services',
                    'module_name': 'Services',
                    'breadcrumbs': ['Backend', 'Services'],
                    'title': 'Backend - Services',
                    'data': LibraryServices.objects.all(),
                    'form': ServicesForm()
                }
                return render(request, 'backend/services.html', context)

        elif action is not None and pk is not None:
            service = LibraryServices.objects.get(id=pk)
            if action == "update":
                if request.method == "GET":
                    context = {
                        'action': 'update_services',
                        'module_name': 'Services',
                        'breadcrumbs': ['Backend', 'Services'],
                        'title': 'Backend - Update Service',
                        'services': LibraryServices.objects.all(),
                        'form': ProcessForm(instance=service),
                        'data': service
                    }
                    return render(request, 'backend/services.html', context)
                elif request.method == "POST":
                    form = ServicesForm(request.POST, instance=service)

                    if form.is_valid():
                        update_form = form.save()
                        update_form.date_updated = datetime.datetime.now()
                        update_form.updated_by = request.user
                        update_form.save()
                        return JsonResponse({'statusMsg': 'Success'}, status=200)

                    return JsonResponse({'statusMsg': 'Invalid!'}, status=404)

    except Exception as e:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            error = ''
            for row in e:
                error = row
            return JsonResponse({'statusMsg': 'error', 'error': error}, status=404)

        messages.success(request, str(e))
        return redirect('backend-services-page')


@login_required(login_url='/login')
def types_page(request, action=None, pk=None):
    try:
        if action is None and pk is None:
            if request.method == "POST":
                form = TypeForm(request.POST)
                if form.is_valid():
                    name = form.clean_type()
                    acronym = form.clean_acronyms()
                    s = form.cleaned_data['status']
                    h = form.cleaned_data['has_worker']
                    i = form.cleaned_data['is_worker']
                    type = LibraryTypes.objects.create(name=name, acronym=acronym, status=s, has_worker=h, is_worker=i,
                                                       created_by=request.user)
                    type.save()
                    return JsonResponse({'statusMsg': 'Success!'}, status=200)
                else:
                    return JsonResponse({'statusMsg': 'Form is invalid!'}, status=404)

            elif request.method == "GET":
                context = {
                    'action': 'types',
                    'module_name': 'Types',
                    'breadcrumbs': ['Backend', 'Types'],
                    'title': 'Backend - Types',
                    'data': LibraryTypes.objects.all(),
                    'form': TypeForm()
                }
                return render(request, 'backend/types.html', context)

        elif action is not None and pk is not None:
            type = LibraryTypes.objects.get(id=pk)
            if action == "update":
                if request.method == "GET":
                    context = {
                        'action': 'update_type',
                        'module_name': 'Types',
                        'breadcrumbs': ['Backend', 'Types'],
                        'title': 'Backend - Update Type',
                        'form': TypeForm(instance=type),
                        'data': type
                    }
                    return render(request, 'backend/types.html', context)

                elif request.method == "POST":
                    form = TypeForm(request.POST, instance=type)

                    if form.is_valid():
                        update_form = form.save()
                        update_form.date_updated = datetime.datetime.now()
                        update_form.updated_by = request.user
                        update_form.save()
                        return JsonResponse({'statusMsg': 'Success'}, status=200)

                    return JsonResponse({'statusMsg': 'Invalid!'}, status=404)
    except Exception as e:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            error = ''
            for row in e:
                error = row
            return JsonResponse({'statusMsg': 'error', 'error': error}, status=404)

        messages.success(request, str(e))
        return redirect('backend-types-page')


@login_required(login_url='/login')
def status_page(request, action=None, pk=None):
    try:
        if action is None and pk is None:
            if request.method == "POST":
                form = StatusForm(request.POST)
                if form.is_valid():
                    name = form.clean_status_name()
                    s = form.cleaned_data['status']
                    status = LibraryStatus.objects.create(name=name, status=s, created_by=request.user)
                    status.save()
                    return JsonResponse({'statusMsg': 'Success!'}, status=200)
                else:
                    return JsonResponse({'statusMsg': 'Form is invalid!'}, status=404)

            elif request.method == "GET":
                context = {
                    'action': 'status',
                    'module_name': 'Status',
                    'breadcrumbs': ['Backend', 'Status'],
                    'title': 'Backend - Status',
                    'data': LibraryStatus.objects.all(),
                    'form': StatusForm()
                }
                return render(request, 'backend/status.html', context)

        elif action is not None and pk is not None:
            status = LibraryStatus.objects.get(id=pk)
            if action == "update":
                if request.method == "GET":
                    context = {
                        'action': 'update_status',
                        'module_name': 'Status',
                        'breadcrumbs': ['Backend', 'Status'],
                        'title': 'Backend - Update Status',
                        'form': StatusForm(instance=status),
                        'data': status
                    }
                    return render(request, 'backend/status.html', context)

                elif request.method == "POST":
                    form = StatusForm(request.POST, instance=status)
                    if form.is_valid():
                        update_form = form.save()
                        update_form.date_updated = datetime.datetime.now()
                        update_form.updated_by = request.user
                        update_form.save()
                        return JsonResponse({'statusMsg': 'Success'}, status=200)

                    return JsonResponse({'statusMsg': 'Invalid!'}, status=404)
    except Exception as e:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            error = ''
            for row in e:
                error = row
            return JsonResponse({'statusMsg': 'error', 'error': error}, status=404)

        messages.success(request, str(e))
        return redirect('backend-types-page')


@login_required(login_url='/login')
def level_page(request, action=None, pk=None):
    try:
        if action is None and pk is None:
            if request.method == "POST":
                form = LevelForm(request.POST)
                if form.is_valid():
                    name = form.clean_level()
                    s = form.cleaned_data['status']
                    level = LibraryLevel.objects.create(name=name, status=s, created_by=request.user)
                    level.save()

                    return JsonResponse({'statusMsg': 'Success!'}, status=200)
                else:
                    return JsonResponse({'statusMsg': 'Form is invalid!'}, status=404)

            elif request.method == "GET":
                context = {
                    'action': 'level',
                    'module_name': 'Level',
                    'breadcrumbs': ['Backend', 'Level'],
                    'title': 'Backend - Level',
                    'data': LibraryLevel.objects.all(),
                    'form': LevelForm()
                }
                return render(request, 'backend/level.html', context)

        elif action is not None and pk is not None:
            level = LibraryLevel.objects.get(id=pk)
            if action == "update":
                if request.method == "GET":
                    context = {
                        'action': 'update_level',
                        'module_name': 'Level',
                        'breadcrumbs': ['Backend', 'Level'],
                        'title': 'Backend - Update Level',
                        'form': LevelForm(instance=level),
                        'data': level
                    }
                    return render(request, 'backend/level.html', context)

                elif request.method == "POST":
                    form = LevelForm(request.POST, instance=level)
                    if form.is_valid():
                        update_form = form.save()
                        update_form.date_updated = datetime.datetime.now()
                        update_form.updated_by = request.user
                        update_form.save()
                        return JsonResponse({'statusMsg': 'Success'}, status=200)

                    return JsonResponse({'statusMsg': 'Invalid!'}, status=404)
    except Exception as e:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            error = ''
            for row in e:
                error = row
            return JsonResponse({'statusMsg': 'error', 'error': error}, status=404)

        messages.success(request, str(e))
        return redirect('backend-level-page')


@login_required(login_url='/login')
def details_attribute_page(request, action=None, pk=None):
    try:
        if action is None and pk is None:
            if request.method == "POST":
                form = DetailsAttributeForm(request.POST)
                if form.is_valid():
                    name = form.cleaned_data['name']
                    input_type = form.cleaned_data['input_type']
                    width = form.cleaned_data['width']
                    order = form.cleaned_data['order']
                    type_id = form.cleaned_data['type']
                    is_required = form.cleaned_data['is_required']
                    details_attribute = DetailsAttribute.objects.create(name=name, input_type=input_type,
                                                                        width=width, order=order, type=type_id,
                                                                        created_by=request.user, is_required=is_required)
                    details_attribute.save()
                    return JsonResponse({'statusMsg': 'Success!'}, status=200)
                else:
                    return JsonResponse({'statusMsg': 'Form is invalid!'}, status=404)

            elif request.method == "GET":
                context = {
                    'action': 'details_attribute',
                    'module_name': 'Details Attribute',
                    'breadcrumbs': ['Backend', 'Details Attribute'],
                    'title': 'Backend - Details Attribute',
                    'data': DetailsAttribute.objects.all(),
                    'form': DetailsAttributeForm()
                }
                return render(request, 'backend/details_attribute.html', context)

        elif action is not None and pk is not None:
            details_attribute = DetailsAttribute.objects.get(id=pk)
            if action == "update":
                if request.method == "GET":
                    context = {
                        'action': 'update_details_attribute',
                        'module_name': 'Details Attribute',
                        'breadcrumbs': ['Backend', 'Details Attribute'],
                        'title': 'Backend - Update Details Attribute',
                        'form': DetailsAttributeForm(instance=details_attribute,
                                                     initial={
                                                         'type': details_attribute.type,
                                                         'status': details_attribute.status}
                                                     ),
                        'data': details_attribute
                    }
                    return render(request, 'backend/details_attribute.html', context)

                elif request.method == "POST":
                    form = DetailsAttributeForm(request.POST, instance=details_attribute)
                    if form.is_valid():
                        update_form = form.save()
                        update_form.date_updated = datetime.datetime.now()
                        update_form.updated_by = request.user
                        update_form.save()
                        return JsonResponse({'statusMsg': 'Success'}, status=200)

                    return JsonResponse({'statusMsg': 'Invalid!'}, status=404)
    except Exception as e:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            error = ''
            for row in e:
                error = row
            return JsonResponse({'statusMsg': 'error', 'error': error}, status=404)

        messages.success(request, str(e))
        return redirect('backend-details-attribute-page')


@login_required(login_url='/login')
def worker_attribute_page(request, action=None, pk=None):
    try:
        if action is None and pk is None:
            if request.method == "POST":
                form = WorkerAttributeForm(request.POST)
                if form.is_valid():
                    name = form.cleaned_data['name']
                    input_type = form.cleaned_data['input_type']
                    width = form.cleaned_data['width']
                    order = form.cleaned_data['order']
                    type_id = form.cleaned_data['type']
                    is_required = form.cleaned_data['is_required']
                    worker_attribute = WorkerAttribute.objects.create(name=name, input_type=input_type,
                                                                      width=width, order=order, type=type_id,
                                                                      created_by=request.user, is_required=is_required)
                    worker_attribute.save()
                    return JsonResponse({'statusMsg': 'Success!'}, status=200)
                else:
                    return JsonResponse({'statusMsg': 'Form is invalid!'}, status=404)

            elif request.method == "GET":
                context = {
                    'action': 'worker_attribute',
                    'module_name': 'Worker Attribute',
                    'breadcrumbs': ['Backend', 'Worker Attribute'],
                    'title': 'Backend - Worker Attribute',
                    'data': WorkerAttribute.objects.all(),
                    'form': WorkerAttributeForm()
                }
                print(WorkerAttributeForm())
                return render(request, 'backend/worker_attribute.html', context)

        elif action is not None and pk is not None:
            worker_attribute = WorkerAttribute.objects.get(id=pk)
            if action == "update":
                if request.method == "GET":
                    context = {
                        'action': 'update_worker_attribute',
                        'module_name': 'Worker Attribute',
                        'breadcrumbs': ['Backend', 'Worker Attribute'],
                        'title': 'Backend - Update Worker Attribute',
                        'form': WorkerAttributeForm(instance=worker_attribute,
                                                    initial={
                                                        'type': worker_attribute.type,
                                                        'status': worker_attribute.status}
                                                    ),
                        'data': worker_attribute
                    }
                    return render(request, 'backend/worker_attribute.html', context)

                elif request.method == "POST":
                    form = WorkerAttributeForm(request.POST, instance=worker_attribute)
                    if form.is_valid():
                        update_form = form.save()
                        update_form.date_updated = datetime.datetime.now()
                        update_form.updated_by = request.user
                        update_form.save()
                        return JsonResponse({'statusMsg': 'Success'}, status=200)

                    return JsonResponse({'statusMsg': 'Invalid!'}, status=404)
    except Exception as e:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            error = ''
            for row in e:
                error = row
            return JsonResponse({'statusMsg': 'error', 'error': error}, status=404)

        messages.success(request, str(e))
        return redirect('backend-worker-attribute-page')


@login_required(login_url='/login')
def get_citymun(request, pk):
    citymuns = LibraryCitymun.objects.filter(prov_code_id=pk).values('code', 'name').order_by('name')
    json = []
    for row in citymuns:
        json.append({row['code']: row['name']})
    return JsonResponse(json, safe=False)


@login_required(login_url='/login')
def get_barangay(request, pk):
    barangays = LibraryBarangay.objects.filter(city_code_id=pk).values('id', 'name').order_by('name')
    json = []
    for row in barangays:
        json.append({row['id']: row['name']})
    return JsonResponse(json, safe=False)
