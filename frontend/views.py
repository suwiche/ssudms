from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction, IntegrityError
from django.db.transaction import rollback
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.db.models import Count
from django.db.models import Q
from backend.forms import Form, VersionsForm
from backend.models import LibraryTypes, DetailsAttribute, WorkerAttribute, LibraryProvince, \
    LibraryExtensions, LibraryStatus, LibraryLevel, LibraryProcess, LibraryStatus, LibraryServices, Forms, \
    LibraryCitymun, LibraryBarangay, LibraryProcessTypes, FormVersions
from .models import Org, OrgDetails, Worker, Transaction, License, WorkerDetails, \
    WorkerTransaction, Logs, AccountSettings, OrgTransaction, OrgService
from .decorators import unauthenticated_user, allowed_users

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta


@login_required(login_url='/login')
def index_page(request):
    try:
        context = {
            'module_name': 'Home',
            'title': 'Home',
            'action': 'dashboard',
            'breadcrumbs': ['Dashboard', 'Home'],
        }
        return render(request, 'frontend/index.html', context)
    except Exception as e:
        print(e)


def update_charts(request, type=None, action=None, year=None):
    try:
        with transaction.atomic():
            if action == "no-filter":
                context = {
                    'action': action,
                    'data': update_charts_lib(year),
                    'type': type
                }
                return render(request, 'dashboard/charts.html', context)
            elif action == "filter":
                return JsonResponse({'data': update_charts_lib(year)})
    except Exception as e:
        print(e)


def update_sms(request):
    try:
        with transaction.atomic():
            data = update_sms_lib()
            return JsonResponse({'data': data}, status=200)
    except Exception as e:
        print(e)


@login_required(login_url='/login')
def account_settings(request, action):
    try:
        if action == "theme":
            num = 1 if int(request.POST.get('num')) == 0 else 0
            settings = AccountSettings.objects.filter(user_id=request.user.id).first()
            if settings:
                settings.theme = num
                settings.save()
                return JsonResponse({'statusMsg': 'Success', 'num': num}, status=200)
            return JsonResponse({'statusMsg': 'Invalid Action!'}, status=404)
    except Exception as e:
        print(e)


@login_required(login_url='/login')
def records(request, acronym=None, action=None):
    try:
        type = LibraryTypes.objects.filter(acronym=acronym).first()
        if type is None:
            return redirect('frontend-records', acronym='cso')
        data = None

        context = {
            'forms': Forms.objects.filter(status=1).all(),
            'data': None,
            'types': LibraryTypes.objects.exclude(id=4),
            'action': 'records',
            'menu_title': 'frontend-records',
            'module_name': 'Records',
            'breadcrumbs': ['User Access', 'Records', type.name],
            'title': 'User Access - Records',
            'acronym': None,
            'p': LibraryProvince.objects.filter(status=1).all(),
            'filters': None,
        }

        if type is not None and action is None:
            # Check if type is Worker
            if not type.is_worker and request.method == "GET":
                # Check if type is SWDA or equal to 3
                data = Org.objects.filter(org_type=type).all() if type.id != 3 else \
                    Org.objects.filter(org_type=type).order_by('-agency_type_id')
                page = request.GET.get('page', 1)
            elif type.is_worker and request.method == "GET":
                data = Worker.objects.filter(org_type=type).all()
                page = request.GET.get('page', 1)

            print(page)
            paginator = Paginator(data, 10)
            context['data'] = paginator.page(page)
            context['acronym'] = acronym
            return render(request, 'frontend/records/records.html', context)

        elif type is not None and action is not None:
            if action == "filter":
                page_num = 1 if not request.GET.get('page') else request.GET.get('page')
                province = None if not request.GET.get('fprovince') else request.GET.get('fprovince')
                city = None if not request.GET.get('fcity') else request.GET.get('fcity')
                barangay = None if not request.GET.get('fbarangay') else request.GET.get('fbarangay')
                keyword = None if not request.GET.get('keyword') else request.GET.get('keyword')
                if not type.is_worker and request.method == "GET":
                    if keyword and province is None and city is None and barangay is None:
                        data = Org.objects.filter(name__icontains=keyword, org_type=type).all() if type.id != 3 else \
                            Org.objects.filter(name__icontains=keyword, org_type=type).all().order_by(
                                '-agency_type_id')
                    elif keyword is None and province is None and city is None and barangay is None:
                        data = Org.objects.filter(org_type=type).all() if type.id != 3 else \
                            Org.objects.filter(name__icontains=keyword, org_type=type).all().order_by(
                                '-agency_type_id')
                    elif keyword and province and city is None and barangay is None:
                        data = Org.objects.filter(name__icontains=keyword, org_type=type,
                                                  barangay__city_code__prov_code_id=province).all() if type.id != 3 else \
                            Org.objects.filter(name__icontains=keyword, org_type=type,
                                               barangay__city_code__prov_code_id=province).all().order_by(
                                '-agency_type_id')
                    elif keyword and province and city and barangay is None:
                        data = Org.objects.filter(name__icontains=keyword, org_type=type,
                                                  barangay__city_code__prov_code_id=province,
                                                  barangay__city_code_id=city).all() if type.id != 3 else \
                            Org.objects.filter(name__icontains=keyword, org_type=type,
                                               barangay__city_code__prov_code_id=province,
                                               barangay__city_code_id=city).all().order_by(
                                '-agency_type_id')
                    elif keyword and province and city and barangay:
                        data = Org.objects.filter(name__icontains=keyword, org_type=type,
                                                  barangay__city_code__prov_code_id=province,
                                                  barangay__city_code_id=city,
                                                  barangay_id=barangay).all() if type.id != 3 else \
                            Org.objects.filter(name__icontains=keyword, org_type=type,
                                               barangay__city_code__prov_code_id=province,
                                               barangay__city_code_id=city, barangay_id=barangay).all().order_by(
                                '-agency_type_id')

                    elif keyword is None and province is None and city is None and barangay is None:
                        data = data = Org.objects.filter(org_type=type).all() if type.id != 3 else \
                            Org.objects.filter(org_type=type).all().order_by(
                                '-agency_type_id')
                
                    context['data'] = Paginator(data, 10).page(page_num)
                    context['acronym'] = acronym
                    context['action'] = 'records_filter'
                    context['filters'] = '?keyword={}&province={}&city={}&barangay={}'.format(keyword, province, city,
                                                                                              barangay)
                    return render(request, 'frontend/records/partials/{}_filter_partial.html'.format(acronym), context)
            else:
                data = Org.objects.all()

        return redirect('frontend-records', acronym='cso')
    except Exception as e:
        print(e)


@login_required(login_url='/login')
def generate_form(request, acronym):
    try:
        if 'new_record' in request.session:
            request.session.pop('new_record')

        request.session['new_record'] = {
            'type_id': None,
            'basic_details': {},
            'additional_details': {},
            'workers': [],
            'license': []
        }
        request.session.modified = True
        is_valid_type = LibraryTypes.objects.get(acronym=acronym)
        if is_valid_type:
            html = '<strong>' + str(acronym) + '</strong>'
            context = {
                'html': html,
                'type': is_valid_type,
                'details_attribute': DetailsAttribute.objects.filter(type__acronym=acronym, status=1).order_by('order'),
                'worker_attribute': WorkerAttribute.objects.filter(type__acronym=acronym, status=1).order_by('order'),
            }
            return render(request, 'frontend/records/generate-form.html', context)
        return JsonResponse({'statusMsg': 'Cannot generate form. Type given is invalid.'}, status=404)
    except Exception as e:
        print(e)


@login_required(login_url='/login')
def add_new_record(request, action):
    sid = transaction.savepoint()
    try:
        if action is not None:
            if request.method == "POST":
                if action == "save-basic-details" or action == "update-basic-details":
                    func_obj = basic_details_session(request, action)
                    return JsonResponse(func_obj[0], status=func_obj[1])

                elif action == "save-additional-details" or action == "update-additional-details":
                    func_obj = additional_details_session(request, action)
                    return JsonResponse(func_obj[0], status=func_obj[1])
                elif action == "save-worker-details" or action == "update-worker-details" or action == "delete-worker-details":
                    func_obj = worker_details_session(request, action)
                    return JsonResponse(func_obj[0], status=func_obj[1])

                elif action == "save-license-details" or action == "update-license-details" or action == "delete-license-details":
                    func_obj = license_details_session(request, action)
                    return JsonResponse(func_obj[0], status=func_obj[1])

                elif action == "save-entry":
                    if 'new_record' in request.session:
                        new_record = request.session['new_record']
                        type = LibraryTypes.objects.filter(id=new_record['type_id']).first()
                        basic_details = new_record['basic_details']
                        additional_details = new_record['additional_details']
                        workers = new_record['workers']
                        license = new_record['license']

                        details = DetailsAttribute.objects.filter(status=1, type=type).all()
                        with transaction.atomic():
                            org = None
                            if not type.is_worker:
                                org = Org(name=basic_details['name'], org_type=type,
                                          created_by=request.user, barangay_id=basic_details['barangay'],
                                          agency_type_id=basic_details['agency_type'])
                                org.save()
                                org_service = OrgService.objects.create(org=org, service_id=basic_details['services'],
                                                                        service_delivery_mode_id=basic_details[
                                                                            'service_mode'])
                                for row in details:
                                    org_details = OrgDetails(
                                        values=additional_details['details-attribute-{}'.format(str(row.id))] if
                                        additional_details else None, org=org, details_attribute=row)
                                    org_details.save()
                            for row in workers:
                                if int(row['status'] == 1):
                                    first_name = row['first_name']
                                    middle_name = row['middle_name']
                                    last_name = row['last_name']
                                    sex = row['sex'] if row['sex'] else 2
                                    extension = row['extension'] if row['extension'] else None
                                    address = row['address']
                                    province = row['province']
                                    worker = Worker(first_name=first_name, middle_name=middle_name, last_name=last_name,
                                                    sex=sex, extension_id=extension,
                                                    org=org if not type.is_worker else None, org_type=type,
                                                    address=address,
                                                    province=province, created_by=request.user)
                                    worker.save()

                                    worker_attributes = WorkerAttribute.objects.filter(status=1, type=type).all()

                                    for i in worker_attributes:
                                        values = row['worker_attributes']['worker-attribute-{}'.format(str(i.id))]
                                        worker_details = WorkerDetails(values=values, worker=worker,
                                                                       worker_attribute_id=i.id)
                                        worker_details.save()
                                    worker_license = row['license']
                                    if worker_license:
                                        process = int(worker_license['process_id'])
                                        date_complete_docs = worker_license['date_complete_docs'] if worker_license[
                                            'date_complete_docs'] else None
                                        date_endorsed = worker_license['date_endorsed'] if worker_license[
                                            'date_endorsed'] else None
                                        date_assessed = worker_license['date_assessed'] if worker_license[
                                            'date_assessed'] else None
                                        date_returned = worker_license['date_returned'] if worker_license[
                                            'date_returned'] else None
                                        assessed_by = worker_license['assessed_by'] if worker_license[
                                            'assessed_by'] else None
                                        remarks = worker_license['remarks'] if worker_license['remarks'] else None
                                        status = int(worker_license['status_id'])
                                        t = Transaction.objects.create(process_id=process, status_id=status,
                                                                       created_by=request.user,
                                                                       last=1, date_complete_docs=date_complete_docs,
                                                                       date_endorsed=date_endorsed,
                                                                       date_assessed=date_assessed,
                                                                       date_returned=date_returned,
                                                                       assessed_by=assessed_by, remarks=remarks)
                                        if status == 4 or status == 5:
                                            level = worker_license['level'] if worker_license['level'] else None
                                            validity = int(worker_license['validity'])
                                            number = worker_license['license_key']
                                            date_issued = worker_license['date_issued']

                                            new_license = License(level_id=level, validity=validity, number=number,
                                                                  date_issued=date_issued,
                                                                  date_expired=date_expired(date_issued, validity),
                                                                  transaction=t)
                                            new_license.save()
                                        worker_transaction = WorkerTransaction(worker=worker, transaction=t)
                                        worker_transaction.save()
                            for row in license:
                                if int(row['status'] == 1):
                                    process = int(row['process_id'])
                                    date_complete_docs = row['date_complete_docs'] if row[
                                        'date_complete_docs'] else None
                                    date_endorsed = row['date_endorsed'] if row['date_endorsed'] else None
                                    date_assessed = row['date_assessed'] if row['date_assessed'] else None
                                    date_returned = row['date_returned'] if row['date_returned'] else None
                                    assessed_by = row['assessed_by'] if row['assessed_by'] else None
                                    status = int(row['status_id'])
                                    process_type = row['process_type_id'] if row['process_type_id'] else None
                                    remarks = row['remarks'] if row['remarks'] else None
                                    t = Transaction.objects.create(process_id=process, status_id=status,
                                                                   created_by=request.user,
                                                                   last=1, date_complete_docs=date_complete_docs,
                                                                   date_endorsed=date_endorsed,
                                                                   date_assessed=date_assessed,
                                                                   date_returned=date_returned,
                                                                   assessed_by=assessed_by,
                                                                   process_type_id=process_type, remarks=remarks)

                                    if status == 4 or status == 5:
                                        level = row['level'] if row['level'] else None
                                        validity = int(row['validity'])
                                        number = row['license_key']
                                        date_issued = row['date_issued']

                                        new_license = License(level_id=level, validity=validity, number=number,
                                                              date_issued=date_issued,
                                                              date_expired=date_expired(date_issued, validity),
                                                              transaction=t)
                                        new_license.save()

                                    org_transaction = OrgTransaction(org=org, transaction=t)
                                    org_transaction.save()

                            # message = 'added new entry for {}(No. {})'.format(org.org_type.name, org.id)
                            # logs(message, request.user, 'Added')

                            return JsonResponse({'statusMsg': 'Entry successfully added.'})
        return redirect('frontend-records')

    except IntegrityError as e:
        transaction.savepoint_rollback(sid)

        return JsonResponse({'statusMsg': str(e)}, status=404)

    except Exception as e:
        print(e)


@login_required(login_url='/login')
def view_record(request, acronym=None, action=None, pk=None):
    try:
        type = LibraryTypes.objects.filter(acronym=acronym).first()
        if not type:
            return redirect('frontend-index-page')
        if acronym is not None and action is None and pk is None:
            if not type.is_worker and request.method == "GET":
                context = {
                    'data': Org.objects.filter(org_type=type).all() if type.id != 3 else Org.objects.filter(
                        org_type=type).order_by('-agency_type_id'),
                    'acronym': acronym
                }
                return render(request, 'frontend/records/{}.html'.format(acronym), context)
            elif type.is_worker and request.method == "GET":
                context = {
                    'data': Worker.objects.filter(org_type=type).all(),
                    'acronym': acronym
                }
                return render(request, 'frontend/records/{}.html'.format(acronym), context)
            else:
                return JsonResponse({'statusMsg': 'Invalid Action!'}, status=404)

        elif acronym is not None and action == "view" and pk is not None:
            if not type.is_worker and request.method == "GET":
                data = Org.objects.filter(id=pk, org_type=type).first()
                if data:
                    context = {
                        'data': data,
                        'action': '{}_view'.format(acronym),
                        'details_attribute': DetailsAttribute.objects.filter(type=type, status=1).order_by('order'),
                        'worker_attribute': WorkerAttribute.objects.filter(type=type, status=1).order_by('order'),
                    }
                    return render(request, 'frontend/records/view-form.html', context)
                return JsonResponse({'statusMsg': 'Invalid Action!'}, status=404)
            elif type.is_worker and request.method == "GET":
                data = Worker.objects.filter(id=pk, org_type=type).first()
                if data:
                    context = {
                        'data': data,
                        'action': '{}_view'.format(acronym),
                        'worker_attribute': WorkerAttribute.objects.filter(type=type, status=1).order_by('order'),
                    }
                    return render(request, 'frontend/records/view-form.html', context)
                return JsonResponse({'statusMsg': 'Invalid Action!'}, status=404)

    except Exception as e:
        print(e)


@require_http_methods(["POST"])
@login_required
@transaction.atomic
def update_record(request, action):
    error = [404, 200]
    sid = transaction.savepoint()
    try:
        with transaction.atomic():
            org = Org.objects.filter(id=request.POST.get('org_id')).first() if request.POST.get('org_id') else None
            if org and action == "update-basic-details":
                name = request.POST.get('name')
                barangay = request.POST.get('barangay')
                service = request.POST.get('services') if request.POST.get('service') else None
                service_mode = request.POST.get('service_mode') if request.POST.get('service_mode') else None
                agency_type = request.POST.get('agency_type') if request.POST.get('agency_type') else None
                org_update = Org.objects.filter(id=org.id).update(name=name, barangay=barangay,
                                                                  agency_type_id=agency_type)
                org_service = OrgService.objects.filter(id=org.id).update(service_delivery_mode=service_mode,
                                                                          service_id=service)

                return JsonResponse({'statusMsg': 'Basic details successfully updated'}, status=200)

            elif org and action == "update-additional-details":
                details = DetailsAttribute.objects.filter(status=1, type=org.org_type).all()
                for row in details:
                    values = request.POST.get('details-attribute-{}'.format(str(row.id)))
                    details_value = OrgDetails.objects.filter(org=org, details_attribute_id=row.id).update(
                        values=values)
                return JsonResponse({'statusMsg': 'Details attribute successfully updated'}, status=200)

            elif org and action == "add-license-details":
                transaction_license = insertLicense(request, org, None, None)
                return JsonResponse(transaction_license[1], status=error[transaction_license[0]])

            elif org and action == "update-license-details":
                process = int(request.POST.get('process'))
                date_complete_docs = request.POST.get('date_complete_docs') if request.POST.get(
                    'date_complete_docs') else None
                date_endorsed = request.POST.get('date_endorsed') if request.POST.get('date_endorsed') else None
                date_assessed = request.POST.get('date_assessed') if request.POST.get('date_assessed') else None
                date_returned = request.POST.get('date_returned') if request.POST.get('date_returned') else None
                assessed_by = request.POST.get('assessed_by') if request.POST.get('assessed_by') else None
                status = int(request.POST.get('status'))
                process_type = request.POST.get('process_type') if request.POST.get('process_type') else None
                remarks = request.POST.get('remarks') if request.POST.get('remarks') else None
                transaction_id = int(request.POST.get('transaction_id')) if request.POST.get(
                    'transaction_id') else None
                license_key = request.POST.get('license_key')
                date_issued = request.POST.get('date_issued')
                validity = request.POST.get('validity')
                level = request.POST.get('level') if request.POST.get('level') else None

                t = Transaction.objects.filter(id=transaction_id).first()
                license = License.objects.filter(transaction=t).first()
                t.status_id = status
                t.process_id = process
                t.date_complete_docs = date_complete_docs
                t.date_endorsed = date_endorsed
                t.date_assessed = date_assessed
                t.date_returned = date_returned
                t.assessed_by = assessed_by
                t.process_type_id = process_type
                t.remarks = remarks
                t.save()

                if status == 4 or status == 5:
                    if license and license_key and date_issued and validity:
                        license.level_id = level if level else None
                        license.validity = validity
                        license.number = license_key
                        license.date_issued = date_issued
                        license.date_expired = date_expired(date_issued, validity)
                        license.transaction = t
                        license.save()

                        return JsonResponse(
                            {'statusMsg': 'License details successfully updated.', 'transaction_id': t.id},
                            status=200)

                    elif not license and license_key and date_issued and validity:

                        new_license = License(level_id=level, validity=int(validity), number=license_key,
                                              date_issued=date_issued,
                                              date_expired=date_expired(date_issued, validity),
                                              transaction=t)
                        new_license.save()

                        return JsonResponse(
                            {'statusMsg': 'License details successfully updated.', 'transaction_id': t.id},
                            status=200)

                    return JsonResponse(
                        {'statusMsg': 'Please fill all fields when status is Active/Inactive.',
                         'transaction_id': t.id},
                        status=404)

                return JsonResponse(
                    {'statusMsg': 'License details successfully updated.', 'transaction_id': t.id},
                    status=200)

            elif action == "add-worker-details":
                first_name = request.POST.get('first_name')
                middle_name = request.POST.get('middle_name')
                last_name = request.POST.get('last_name')
                sex = request.POST.get('sex') if request.POST.get('sex') else 2
                extension_id = request.POST.get('ext_name')
                type_id = request.POST.get('type_id')
                address = request.POST.get('address')
                province = request.POST.get('province')
                worker = Worker(first_name=first_name, middle_name=middle_name,
                                last_name=last_name, sex=sex, extension_id=extension_id, address=address,
                                province=province, org=org, org_type_id=org.org_type.id)
                worker.save()
                worker_attributes = WorkerAttribute.objects.filter(status=1, type_id=org.org_type.id).all()
                for i in worker_attributes:
                    values = request.POST.get('worker-attribute-{}'.format(str(i.id)))
                    worker_details = WorkerDetails(values=values, worker=worker,
                                                   worker_attribute_id=i.id)
                    worker_details.save()
                if org.org_type.acronym == "cdc":
                    transaction_license = insertLicense(request, org, 'worker', worker)
                    if transaction_license[0] == 0:
                        raise IntegrityError(transaction_license[1]['statusMsg'])
                    return JsonResponse(transaction_license[1], status=error[transaction_license[0]])

                return JsonResponse({'statusMsg': 'Worker successfully added.'}, status=200)

            elif action == "update-worker-details":
                worker_id = request.POST.get('worker_id')
                worker = Worker.objects.filter(id=worker_id).first()
                worker.first_name = request.POST.get('first_name')
                worker.middle_name = request.POST.get('middle_name')
                worker.last_name = request.POST.get('last_name')
                worker.sex = request.POST.get('sex') if request.POST.get('sex') else 2
                worker.extension_id = request.POST.get('ext_name')
                worker.address = request.POST.get('address')
                worker.province = request.POST.get('province')
                worker.save()
                worker_attributes = WorkerAttribute.objects.filter(status=1, type_id=request.POST.get('type_id')).all()
                for i in worker_attributes:
                    values = request.POST.get('worker-attribute-{}'.format(str(i.id)))
                    worker_value = WorkerDetails.objects.filter(worker=worker, worker_attribute_id=i.id).update(
                        values=values)

                process = int(request.POST.get('worker_process')) if request.POST.get('worker_process') else None
                if process:
                    date_complete_docs = request.POST.get('wdate_complete_docs') if request.POST.get(
                        'wdate_complete_docs') else None
                    date_endorsed = request.POST.get('wdate_endorsed') if request.POST.get(
                        'wdate_endorsed') else None
                    date_assessed = request.POST.get('wdate_assessed') if request.POST.get(
                        'wdate_assessed') else None
                    date_returned = request.POST.get('wdate_returned') if request.POST.get(
                        'wdate_returned') else None
                    assessed_by = request.POST.get('wassessed_by') if request.POST.get('wassessed_by') else None
                    remarks = request.POST.get('remarks') if request.POST.get('remarks') else None
                    status = int(request.POST.get('worker_status'))
                    transaction_id = int(request.POST.get('transaction_id')) if request.POST.get(
                        'transaction_id') else None
                    license_key = request.POST.get('worker_license_key')
                    date_issued = request.POST.get('worker_date_issued')
                    validity = request.POST.get('worker_validity')
                    level = request.POST.get('worker_level') if request.POST.get('worker_level') else None
                    t = Transaction.objects.filter(id=transaction_id).first()

                    license = License.objects.filter(transaction=t).first()

                    t.process_id = process
                    t.date_complete_docs = date_complete_docs
                    t.date_endorsed = date_endorsed
                    t.date_assessed = date_assessed
                    t.date_returned = date_returned
                    t.assessed_by = assessed_by
                    t.remarks = remarks
                    t.save()

                    if status == 4 or status == 5:
                        if license and license_key and date_issued and validity:

                            t.status_id = status
                            t.save()
                            license.level_id = level
                            license.validity = validity
                            license.number = license_key
                            license.date_issued = date_issued
                            license.date_expired = date_expired(date_issued, validity)
                            license.save()
                            return JsonResponse(
                                {'statusMsg': 'Worker details successfully updated.', 'transaction_id': t.id},
                                status=200)

                        elif not license and license_key and date_issued and validity:

                            t.status_id = status
                            t.save()

                            new_license = License(level_id=level if level else None, validity=int(validity),
                                                  number=license_key, date_issued=date_issued,
                                                  date_expired=date_expired(date_issued, validity),
                                                  transaction=t)
                            new_license.save()

                            return JsonResponse(
                                {'statusMsg': 'Worker details successfully updated.', 'transaction_id': t.id},
                                status=200)
                        return JsonResponse(
                            {'statusMsg': 'Please fill all fields when status is Active/Inactive.',
                             'transaction_id': t.id},
                            status=404)

                    return JsonResponse(
                        {'statusMsg': 'Worker details successfully updated.', 'transaction_id': t.id},
                        status=200)

                return JsonResponse(
                    {'statusMsg': 'Worker details successfully updated.', 'transaction_id': None},
                    status=200)

    except IntegrityError as e:
        transaction.savepoint_rollback(sid)
        return JsonResponse({'statusMsg': str(e)}, status=404)

    except Exception as e:
        print(e)


@login_required(login_url='/login')
def forms_page(request, action=None, pk=None):
    try:
        if action is None and pk is None:
            if request.method == "POST":
                form = Form(request.POST)
                if form.is_valid():
                    name = form.clean_form_name()
                    s = form.cleaned_data['status']
                    org_type = form.cleaned_data['org_type']
                    orientation = form.cleaned_data['orientation']
                    form_type = form.cleaned_data['form_type']
                    form = Forms.objects.create(name=name, status=s, org_type=org_type, orientation=orientation,
                                                form_type=form_type, created_by=request.user)
                    form.save()

                    return JsonResponse({'statusMsg': 'Success!'}, status=200)
                else:
                    return JsonResponse({'statusMsg': 'Form is invalid!'}, status=404)

            elif request.method == "GET":
                context = {
                    'action': 'form',
                    'module_name': 'Forms',
                    'breadcrumbs': ['Frontend', 'Forms'],
                    'title': 'Frontend - Form',
                    'data': Forms.objects.filter(status=1),
                    'form': Form()
                }
                return render(request, 'frontend/forms/form.html', context)

        elif action is not None and pk is not None:
            form = Forms.objects.get(id=pk)
            if action == "update":
                if request.method == "GET":
                    context = {
                        'action': 'update_form',
                        'module_name': 'Forms',
                        'breadcrumbs': ['Frontend', 'Forms'],
                        'title': 'Frontend - Update Form',
                        'form': Form(instance=form),
                        'data': form
                    }
                    return render(request, 'frontend/forms/form.html', context)

                elif request.method == "POST":
                    form = Form(request.POST, instance=form)
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
        return redirect('frontend-forms')


@login_required(login_url='/login')
def forms_versions_page(request, action=None, pk=None):
    try:
        if action is None and pk is None:
            if request.method == "POST":
                form = VersionsForm(request.POST)
                if form.is_valid():
                    name = form.clean_form_version_name()
                    s = form.cleaned_data['status']
                    template = form.cleaned_data['template']
                    form_d = form.cleaned_data['form']
                    form = FormVersions.objects.create(name=name, status=s, form=form_d, template=template, created_by=request.user)
                    form.save()

                    return JsonResponse({'statusMsg': 'Success!'}, status=200)
                else:
                    return JsonResponse({'statusMsg': 'Form is invalid!'}, status=404)

            elif request.method == "GET":
                context = {
                    'action': 'form_versions',
                    'module_name': 'Versions',
                    'breadcrumbs': ['Frontend', 'Forms', 'Versions'],
                    'title': 'Frontend - Form Versions',
                    'data': FormVersions.objects.filter(status=1),
                    'form': VersionsForm()
                }
                return render(request, 'frontend/forms/versions.html', context)

        elif action is not None and pk is not None:
            form = FormVersions.objects.get(id=pk)
            if action == "update":
                if request.method == "GET":
                    context = {
                        'action': 'update_version',
                        'module_name': 'Versions',
                        'breadcrumbs': ['Frontend', 'Forms', 'Version'],
                        'title': 'Frontend - Update Form Versions',
                        'form': VersionsForm(instance=form),
                        'data': form
                    }
                    return render(request, 'frontend/forms/versions.html', context)

                elif request.method == "POST":
                    form = VersionsForm(request.POST, instance=form)
                    if form.is_valid():
                        update_form = form.save()
                        update_form.date_updated = date.today()
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
        return redirect('frontend-forms-versions')


@login_required(login_url='/login')
def generate_report(request, type=None, filter=None):
    quarters = {
        '1': [1, 3],
        '2': [4, 6],
        '3': [7, 9],
        '4': [10, 12]
    }
    wquarters = ['1st', '2nd', '3rd', '4th']
    if type is not None and filter is None:
        pass

    elif type is not None and filter is None:
        pass
    try:
        if request.method == "POST":
            quarters = {
                '1': [1, 3],
                '2': [4, 6],
                '3': [7, 9],
                '4': [10, 12]
            }
            wquarters = ['1st', '2nd', '3rd', '4th']
            form_id = request.POST.get('form')
            id_quarter = int(request.POST.get('quarter'))
            id_year = int(request.POST.get('year'))
            action = request.POST.get('action')
            data = None
            form = Forms.objects.filter(id=form_id).first()
            if action == "load" and form:
                if form.name == "SB-FORM-003-A":
                    data = Org.objects.filter(
                        Q(orgtransaction__transaction__status_id=3) |
                        Q(orgtransaction__transaction__status_id=4) |
                        Q(orgtransaction__transaction__status_id=5),
                        orgtransaction__transaction__last=1,
                        orgtransaction__transaction__process_id=2, org_type_id=3,
                        orgtransaction__transaction__date_assessed__year=id_year,
                        orgtransaction__transaction__date_assessed__month__range=(
                            quarters['{}'.format(id_quarter)][0], quarters['{}'.format(id_quarter)][1])).exclude(
                        orgtransaction__transaction__assessed_by=None,
                        orgtransaction__transaction__date_assessed=None).all()
                elif form.name == "SB-FORM-002-A":
                    data = Org.objects.filter(Q(orgtransaction__transaction__status_id=3) |
                                              Q(orgtransaction__transaction__status_id=4) |
                                              Q(orgtransaction__transaction__status_id=5),
                                              orgtransaction__transaction__last=1,
                                              orgtransaction__transaction__process_id=1, org_type_id=3,
                                              orgtransaction__transaction__date_assessed__year=id_year,
                                              orgtransaction__transaction__date_assessed__month__range=(
                                                  quarters['{}'.format(id_quarter)][0],
                                                  quarters['{}'.format(id_quarter)][1])).exclude(
                        orgtransaction__transaction__assessed_by=None,
                        orgtransaction__transaction__date_assessed=None).all()
                elif form.name == "SB-FORM-004-A":
                    data = Org.objects.filter(Q(orgtransaction__transaction__status_id=3) |
                                              Q(orgtransaction__transaction__status_id=4) |
                                              Q(orgtransaction__transaction__status_id=5),
                                              orgtransaction__transaction__last=1,
                                              orgtransaction__transaction__process_id=3, org_type_id=2,
                                              orgtransaction__transaction__date_assessed__year=id_year,
                                              orgtransaction__transaction__date_assessed__month__range=(
                                                  quarters['{}'.format(id_quarter)][0],
                                                  quarters['{}'.format(id_quarter)][1])).exclude(
                        orgtransaction__transaction__assessed_by=None,
                        orgtransaction__transaction__date_assessed=None).all()

                elif form.name == "SB-FORM-005-A":
                    data = Worker.objects.filter(Q(workertransaction__transaction__status_id=3) |
                                                 Q(workertransaction__transaction__status_id=4) |
                                                 Q(workertransaction__transaction__status_id=5),
                                                 workertransaction__transaction__last=1,
                                                 workertransaction__transaction__process_id=3, org_type_id=6,
                                                 workertransaction__transaction__date_assessed__year=id_year,
                                                 workertransaction__transaction__date_assessed__month__range=(
                                                     quarters['{}'.format(id_quarter)][0],
                                                     quarters['{}'.format(id_quarter)][1])).exclude(
                        workertransaction__transaction__assessed_by=None,
                        workertransaction__transaction__date_assessed=None).all()

                elif form.name == "SB-FORM-005-B":
                    data = Worker.objects.filter(Q(workertransaction__transaction__status_id=2) |
                                                 Q(workertransaction__transaction__status_id=3) |
                                                 Q(workertransaction__transaction__status_id=4) |
                                                 Q(workertransaction__transaction__status_id=5),
                                                 workertransaction__transaction__last=1,
                                                 workertransaction__transaction__process_id=3, org_type_id=5,
                                                 workertransaction__transaction__date_assessed__year=id_year,
                                                 workertransaction__transaction__date_assessed__month__range=(
                                                     quarters['{}'.format(id_quarter)][0],
                                                     quarters['{}'.format(id_quarter)][1])).exclude(
                        workertransaction__transaction__assessed_by=None,
                        workertransaction__transaction__date_assessed=None).all()

                context = {
                    'data': data,
                    'action': action,
                    'quarter': wquarters[id_quarter - 1],
                    'year': id_year
                }
                return render(request, 'frontend/forms/{}.html'.format(form.name), context)

        context = {
            'module_name': 'Generate Report',
            'title': 'Generate Report',
            'action': 'generate-report',
            'breadcrumbs': ['Generate Report'],
            'forms': Forms.objects.filter(status=1, orientation="landscape").all(),
        }

        return render(request, 'frontend/records/generate-report.html', context)
    except Exception as e:
        print(e)


@login_required(login_url='/login')
def summary_report(request):
    try:
        if request.method == "POST":
            id_type = request.POST.get('id_type')
            type = LibraryTypes.objects.filter(id=id_type).first()
            if type:
                quarters = {
                    '1': [1, 3],
                    '2': [4, 6],
                    '3': [7, 9],
                    '4': [10, 12]
                }
                id_status = request.POST.get('id_status')
                id_process = request.POST.get('id_process')
                id_quarter = quarters[request.POST.get('id_quarter')] if request.POST.get(
                    'id_quarter') != "all" else 'all'
                id_year = request.POST.get('id_year')
                id_province = request.POST.get('id_province')
                data = None
                # province = LibraryProvince.objects.filter(id=id_province, status=1).first()
                # print(province)
                if not type.is_worker and id_year and id_process and id_status == "all" and id_province == "all" and id_quarter == "all":
                    data = Org.objects.filter(org_type=type, barangay__city_code__prov_code__status=1,
                                              orgtransaction__transaction__last=1,
                                              orgtransaction__transaction__process_id=id_process,
                                              orgtransaction__transaction__license__date_issued__year=id_year).order_by(
                        '-orgtransaction__id')

                elif not type.is_worker and id_year and id_process and id_status == "all" and id_province == "all" and id_quarter != "all":
                    data = Org.objects.filter(org_type=type, barangay__city_code__prov_code__status=1,
                                              orgtransaction__transaction__last=1,
                                              orgtransaction__transaction__process_id=id_process,
                                              orgtransaction__transaction__license__date_issued__year=id_year,
                                              orgtransaction__transaction__license__date_issued__month__range=(
                                                  id_quarter[0], id_quarter[1])
                                              ).order_by('-orgtransaction__id')

                elif not type.is_worker and id_year and id_process and id_status == "all" and id_province != "all" and id_quarter != "all":
                    data = Org.objects.filter(org_type=type, barangay__city_code__prov_code__id=id_province,
                                              orgtransaction__transaction__last=1,
                                              orgtransaction__transaction__process_id=id_process,
                                              orgtransaction__transaction__license__date_issued__year=id_year,
                                              orgtransaction__transaction__license__date_issued__month__range=(
                                                  id_quarter[0], id_quarter[1])
                                              ).order_by('-orgtransaction__id')

                elif not type.is_worker and id_year and id_process and id_status != "all" and id_province != "all" and id_quarter != "all":
                    data = Org.objects.filter(org_type=type, barangay__city_code__prov_code__id=id_province,
                                              orgtransaction__transaction__last=1,
                                              orgtransaction__transaction__status_id=id_status,
                                              orgtransaction__transaction__process_id=id_process,
                                              orgtransaction__transaction__license__date_issued__year=id_year,
                                              orgtransaction__transaction__license__date_issued__month__range=(
                                                  id_quarter[0], id_quarter[1])
                                              ).order_by('-orgtransaction__id')

                elif not type.is_worker and id_year and id_process and id_status != "all" and id_province != "all" and id_quarter == "all":
                    data = Org.objects.filter(org_type=type, barangay__city_code__prov_code__id=id_province,
                                              orgtransaction__transaction__last=1,
                                              orgtransaction__transaction__status_id=id_status,
                                              orgtransaction__transaction__process_id=id_process,
                                              orgtransaction__transaction__license__date_issued__year=id_year
                                              ).order_by('-orgtransaction__id')

                elif not type.is_worker and id_year and id_process and id_status == "all" and id_province != "all" and id_quarter == "all":
                    data = Org.objects.filter(org_type=type, barangay__city_code__prov_code__id=id_province,
                                              orgtransaction__transaction__last=1,
                                              orgtransaction__transaction__process_id=id_process,
                                              orgtransaction__transaction__license__date_issued__year=id_year
                                              ).order_by('-orgtransaction__id')

                elif not type.is_worker and id_year and id_process and id_status != "all" and id_province == "all" and id_quarter != "all":
                    data = Org.objects.filter(org_type=type, barangay__city_code__prov_code__status=1,
                                              orgtransaction__transaction__last=1,
                                              orgtransaction__transaction__status_id=id_status,
                                              orgtransaction__transaction__process_id=id_process,
                                              orgtransaction__transaction__license__date_issued__year=id_year,
                                              orgtransaction__transaction__license__date_issued__month__range=(
                                                  id_quarter[0], id_quarter[1])
                                              ).order_by('-orgtransaction__id')

                elif not type.is_worker and id_year and id_process and id_status != "all" and id_province == "all" and id_quarter == "all":
                    data = Org.objects.filter(org_type=type,
                                              barangay__city_code__prov_code__status=1,
                                              orgtransaction__transaction__last=1,
                                              orgtransaction__transaction__status_id=id_status,
                                              orgtransaction__transaction__process_id=id_process,
                                              orgtransaction__transaction__license__date_issued__year=id_year).order_by(
                        '-orgtransaction__id')

                elif type.is_worker and id_year and id_process and id_status == "all" and id_province == "all" and id_quarter == "all":
                    data = Org.objects.filter(org_type=type,
                                              workertransaction__transaction__last=1,
                                              workertransaction__transaction__process_id=id_process,
                                              workertransaction__transaction__license__date_issued__year=id_year).order_by(
                        '-workertransaction')

                elif type.is_worker and id_year and id_process and id_status == "all" and id_province == "all" and id_quarter != "all":
                    data = Org.objects.filter(org_type=type,
                                              workertransaction__transaction__last=1,
                                              workertransaction__transaction__process_id=id_process,
                                              workertransaction__transaction__license__date_issued__year=id_year,
                                              workertransaction__transaction__license__date_issued__month__range=(
                                                  id_quarter[0], id_quarter[1])
                                              ).order_by('-workertransaction')

                elif type.is_worker and id_year and id_process and id_status == "all" and id_province != "all" and id_quarter != "all":
                    province = LibraryProvince.objects.filter(id=id_province, status=1).first()
                    data = Org.objects.filter(org_type=type,
                                              province__icontains=province.name,
                                              workertransaction__transaction__last=1,
                                              workertransaction__transaction__process_id=id_process,
                                              workertransaction__transaction__license__date_issued__year=id_year,
                                              workertransaction__transaction__license__date_issued__month__range=(
                                                  id_quarter[0], id_quarter[1])
                                              ).order_by('-workertransaction__id')

                elif type.is_worker and id_year and id_process and id_status != "all" and id_province != "all" and id_quarter != "all":
                    province = LibraryProvince.objects.filter(id=id_province, status=1).first()
                    data = Org.objects.filter(org_type=type,
                                              province__icontains=province.name,
                                              workertransaction__transaction__last=1,
                                              workertransaction__transaction__status_id=id_status,
                                              workertransaction__transaction__process_id=id_process,
                                              workertransaction__transaction__license__date_issued__year=id_year,
                                              workertransaction__transaction__license__date_issued__month__range=(
                                                  id_quarter[0], id_quarter[1])
                                              ).order_by('-workertransaction__id')

                elif type.is_worker and id_year and id_process and id_status != "all" and id_province != "all" and id_quarter == "all":
                    province = LibraryProvince.objects.filter(id=id_province, status=1).first()
                    data = Org.objects.filter(org_type=type,
                                              province__icontains=province.name,
                                              workertransaction__transaction__last=1,
                                              workertransaction__transaction__status_id=id_status,
                                              workertransaction__transaction__process_id=id_process,
                                              workertransaction__transaction__license__date_issued__year=id_year
                                              ).order_by('-workertransaction__id')

                elif type.is_worker and id_year and id_process and id_status == "all" and id_province != "all" and id_quarter == "all":
                    province = LibraryProvince.objects.filter(id=id_province, status=1).first()
                    data = Org.objects.filter(org_type=type,
                                              province__icontains=province.name,
                                              workertransaction__transaction__last=1,
                                              workertransaction__transaction__process_id=id_process,
                                              workertransaction__transaction__license__date_issued__year=id_year
                                              ).order_by('-workertransaction__id')

                elif type.is_worker and id_year and id_process and id_status != "all" and id_province == "all" and id_quarter != "all":
                    data = Org.objects.filter(org_type=type,
                                              workertransaction__transaction__last=1,
                                              workertransaction__transaction__status_id=id_status,
                                              workertransaction__transaction__process_id=id_process,
                                              workertransaction__transaction__license__date_issued__year=id_year,
                                              workertransaction__transaction__license__date_issued__month__range=(
                                                  id_quarter[0], id_quarter[1])
                                              ).order_by('-workertransaction__id')

                elif type.is_worker and id_year and id_process and id_status != "all" and id_province == "all" and id_quarter == "all":
                    data = Worker.objects.filter(org_type=type,
                                                 workertransaction__transaction__last=1,
                                                 workertransaction__transaction__status_id=id_status,
                                                 workertransaction__transaction__process_id=id_process,
                                                 workertransaction__transaction__license__date_issued__year=id_year).order_by(
                        '-workertransaction__id')

                context = {
                    'data': data,
                    'year': id_year,
                    'type': type
                }
                return render(request, 'frontend/summary-report/{}-summary-report.html'.format(type.acronym), context)

        context = {
            'module_name': 'Summary Report',
            'title': 'Summary Report',
            'action': 'summary-report',
            'breadcrumbs': ['Summary Report'],
            'org_types': LibraryTypes.objects.filter(status=1).all()
        }
        return render(request, 'frontend/records/summary-report.html', context)
    except Exception as e:
        print(e)


def logs(message, user, action):
    Logs.objects.create(message=message, created_by=user, action=action)
    pass


def insertLicense(request, org, type, worker):
    try:
        sid = transaction.savepoint()
        with transaction.atomic():
            process = int(request.POST.get('process'))
            status = int(request.POST.get('status'))
            date_complete_docs = request.POST.get('date_complete_docs') if request.POST.get('date_complete_docs') \
                else None
            date_endorsed = request.POST.get('date_endorsed') if request.POST.get('date_endorsed') else None
            date_assessed = request.POST.get('date_assessed') if request.POST.get('date_assessed') else None
            date_returned = request.POST.get('date_returned') if request.POST.get('date_returned') else None
            assessed_by = request.POST.get('assessed_by') if request.POST.get('assessed_by') else None
            process_type = request.POST.get('process_type') if request.POST.get('process_type') else None
            remarks = request.POST.get('remarks') if request.POST.get('remarks') else None
            if type != "worker":
                old_transaction = OrgTransaction.objects.filter(org=org, transaction__process_id=process,
                                                                transaction__last=1).first()
                if old_transaction:
                    old_transaction.transaction.last = 0
                    old_transaction.transaction.save()

            t = Transaction.objects.create(process_id=process, status_id=status,
                                           created_by=request.user,
                                           last=1, date_complete_docs=date_complete_docs,
                                           date_endorsed=date_endorsed,
                                           date_assessed=date_assessed,
                                           date_returned=date_returned,
                                           assessed_by=assessed_by,
                                           process_type_id=process_type, remarks=remarks)

            if type == 'worker':
                worker_transaction = WorkerTransaction(worker=worker, transaction=t)
                worker_transaction.save()
            else:
                org_transaction = OrgTransaction(org=org, transaction=t)
                org_transaction.save()

            if status == 4 or status == 5:
                license_key = request.POST.get('license_key')
                date_issued = request.POST.get('date_issued')
                level = request.POST.get('level')
                validity = request.POST.get('validity')
                if license_key and date_issued and validity:

                    if isinstance(int(validity), int):
                        validity = int(validity)
                    else:
                        raise IntegrityError('Please input number only in Validity field.')

                    new_license = License(level_id=level if level else None, validity=validity,
                                          number=license_key, date_issued=date_issued,
                                          date_expired=date_expired(date_issued, validity), transaction=t)
                    new_license.save()

                else:
                    raise IntegrityError('Please fill all fields when status is Active/Inactive.')

            return [1, {'statusMsg': 'License details successfully added.', 'transaction_id': t.id}]

    except IntegrityError as e:
        transaction.savepoint_rollback(sid)
        return [0, {'statusMsg': str(e)}]

    except Exception as e:
        transaction.savepoint_rollback(sid)
        return [0, {'statusMsg': str(e)}]


def date_expired(date_issued, validity):
    date_format = '%Y/%m/%d'
    dtObj = datetime.strptime(date_issued.replace('-', '/'), date_format)
    future_date = dtObj + relativedelta(months=int(validity))
    return future_date.date() + timedelta(days=1)


def basic_details_session(request, action):
    type = LibraryTypes.objects.filter(id=request.POST.get('type_id')).first()
    if action == "save-basic-details" or action == "update-basic-details" and 'new_record' in request.session and type:
        request.session['new_record']['type_id'] = type.id
        request.session['new_record']['basic_details'].update(
            {
                'name': request.POST.get('name'),
                'barangay': request.POST.get('barangay'),
                'services': request.POST.get('services') if request.POST.get('services') else None,
                'service_mode': request.POST.get('service_mode') if request.POST.get('service_mode') else None,
                'agency_type': request.POST.get('agency_type') if request.POST.get('agency_type') else None
            }
        )
        request.session.modified = True
        return [{'statusMsg': 'Basic details successfully added/updated'}, 200]

    return ['Invalid Action!', 404]


def additional_details_session(request, action):
    type = LibraryTypes.objects.filter(id=request.POST.get('type_id')).first()
    details = DetailsAttribute.objects.filter(status=1, type=type).all()
    if action == "save-additional-details" or action == "update-additional-details" and type and details and 'new_record' in request.session and 'additional_details' in \
            request.session['new_record']:
        request.session['new_record']['type_id'] = type.id
        for row in details:
            request.session['new_record']['additional_details'][
                'details-attribute-{}'.format(str(row.id))] = request.POST.get(
                'details-attribute-' + str(row.id))
        request.session.modified = True
        return [{'statusMsg': 'Additional details successfully added/updated'}, 200]
    return ['Invalid Action!', 404]


def worker_details_session(request, action):
    type = LibraryTypes.objects.filter(id=request.POST.get('type_id')).first()
    worker_attributes = WorkerAttribute.objects.filter(status=1, type=type).all()
    license_dict = {}
    worker_attr_dict = {}
    if action == "save-worker-details" or action == "update-worker-details" and type and 'new_record' in request.session and 'workers' in \
            request.session['new_record']:
        request.session['new_record']['type_id'] = type.id
        if type.id == 2 or type.is_worker:
            license_dict = {
                'process_id': request.POST.get('worker_process'),
                'date_complete_docs': request.POST.get('wdate_complete_docs'),
                'date_endorsed': request.POST.get('wdate_endorsed'),
                'date_assessed': request.POST.get('wdate_assessed'),
                'date_returned': request.POST.get('wdate_returned'),
                'assessed_by': request.POST.get('wassessed_by'),
                'status_id': request.POST.get('worker_status'),
                'license_key': request.POST.get('worker_license_key'),
                'date_issued': request.POST.get('worker_date_issued'),
                'validity': request.POST.get('worker_validity'),
                'level': request.POST.get('worker_level') if request.POST.get('worker_level') else None,
                'remarks': request.POST.get('worker_remarks')
            }
        for row in worker_attributes:
            worker_attr_dict['worker-attribute-{}'.format(str(row.id))] = request.POST.get(
                'worker-attribute-' + str(row.id))
        if action == "save-worker-details":
            request.session['new_record']['workers'].append({
                'first_name': request.POST.get('first_name'),
                'middle_name': request.POST.get('middle_name'),
                'last_name': request.POST.get('last_name'),
                'extension': request.POST.get('ext_name') if request.POST.get('ext_name') else None,
                'sex': request.POST.get('sex') if request.POST.get('sex') else None,
                'address': request.POST.get('address'),
                'province': request.POST.get('province'),
                'worker_attributes': worker_attr_dict,
                'license': license_dict,
                'status': 1
            })
            request.session.modified = True
            return [{'statusMsg': 'Contact person details successfully added.',
                     'worker_count': int(len(request.session['new_record']['workers'])) - 1}, 200]

        elif action == "update-worker-details":
            worker_count = int(request.POST.get('worker_count'))
            request.session['new_record']['workers'][worker_count] = {
                'first_name': request.POST.get('first_name'),
                'middle_name': request.POST.get('middle_name'),
                'last_name': request.POST.get('last_name'),
                'extension': request.POST.get('ext_name') if request.POST.get('ext_name') else None,
                'sex': request.POST.get('sex') if request.POST.get('sex') else None,
                'address': request.POST.get('address'),
                'province': request.POST.get('province'),
                'worker_attributes': worker_attr_dict,
                'license': license_dict,
                'status': 1
            }
            request.session.modified = True
            return [{'statusMsg': 'Contact person details successfully updated.', 'worker_count': worker_count}, 200]

    elif action == "delete-worker-details" and 'new_record' in request.session and 'workers' in request.session[
        'new_record']:
        worker_count = int(request.POST.get('worker_count')) if request.POST.get('worker_count') else None
        if worker_count and worker_count >= 0:
            request.session['new_record']['workers'][worker_count]['status'] = 0
            request.session.modified = True
        return [{'statusMsg': 'Contact person details successfully deleted.'}, 200]

    return ['Invalid Action!', 404]


def license_details_session(request, action):
    if action == "save-license-details" or action == "update-license-details" and 'new_record' in request.session and 'license' in \
            request.session['new_record']:
        if action == "save-license-details":
            request.session['new_record']['license'].append({
                'process_id': request.POST.get('process'),
                'date_complete_docs': request.POST.get('date_complete_docs'),
                'date_endorsed': request.POST.get('date_endorsed'),
                'date_assessed': request.POST.get('date_assessed'),
                'date_returned': request.POST.get('date_returned'),
                'assessed_by': request.POST.get('assessed_by'),
                'status_id': request.POST.get('status'),
                'license_key': request.POST.get('license_key'),
                'date_issued': request.POST.get('date_issued'),
                'validity': request.POST.get('validity'),
                'level': request.POST.get('level'),
                'process_type_id': request.POST.get('process_type'),
                'remarks': request.POST.get('remarks'),
                'status': 1
            })
            request.session.modified = True
            return [{'statusMsg': 'Transaction details successfully added.',
                     'license_count': int(len(request.session['new_record']['license'])) - 1},
                    200]
        elif action == "update-license-details":
            license_count = int(request.POST.get('license_count'))
            request.session['new_record']['license'][license_count] = {
                'process_id': request.POST.get('process'),
                'date_complete_docs': request.POST.get('date_complete_docs'),
                'date_endorsed': request.POST.get('date_endorsed'),
                'date_assessed': request.POST.get('date_assessed'),
                'date_returned': request.POST.get('date_returned'),
                'assessed_by': request.POST.get('assessed_by'),
                'status_id': request.POST.get('status'),
                'license_key': request.POST.get('license_key'),
                'date_issued': request.POST.get('date_issued'),
                'validity': request.POST.get('validity'),
                'level': request.POST.get('level'),
                'process_type_id': request.POST.get('process_type'),
                'remarks': request.POST.get('remarks'),
                'status': 1
            }
            request.session.modified = True
            return [{'statusMsg': 'Transaction details successfully updated.', 'license_count': license_count}, 200]

    elif action == "delete-license-details" and 'new_record' in request.session and 'license' in request.session[
        'new_record']:
        license_count = int(request.POST.get('license_count')) if request.POST.get('license_count') else None
        if license_count and license_count >= 0:
            request.session['new_record']['license'][license_count]['status'] = 0
            request.session.modified = True
        return [{'statusMsg': 'Transaction details successfully deleted.'}, 200]
    return ['Invalid Action!', 404]


def update_charts_lib(year):
    try:
        with transaction.atomic():
            data = {
                'cso': {
                    'accreditation': {
                        'active': [],
                        'inactive': []
                    }
                },
                'cdc': {
                    'accreditation': {
                        'active': [],
                        'inactive': []
                    }
                },
                'cdw': {
                    'accreditation': {
                        'active': [],
                        'inactive': []
                    }
                },
                'swda': {
                    'registration': {
                        'active': [],
                        'inactive': []
                    },
                    'licensing': {
                        'active': [],
                        'inactive': []
                    },
                    'accreditation': {
                        'active': [],
                        'inactive': []
                    }
                },
                'swmcc': {
                    'accreditation': {
                        'active': [],
                        'inactive': []
                    }
                },
                'pmc': {
                    'accreditation': {
                        'active': [],
                        'inactive': []
                    }
                },
                'scc': {
                    'accreditation': {
                        'active': [],
                        'inactive': []
                    }
                },
                'ps': {
                    'accreditation': {
                        'active': [],
                        'inactive': []
                    }
                }
            }

            quarters = [
                [1, 3],
                [4, 6],
                [7, 9],
                [10, 12]
            ]

            types = LibraryTypes.objects.filter(status=1).exclude(id=4).all()
            for t in types:
                if not t.is_worker:
                    for row in quarters:
                        active = Org.objects.filter(org_type=t, barangay__city_code__prov_code__status=1,
                                                    orgtransaction__transaction__status_id=4,
                                                    orgtransaction__transaction__last=1,
                                                    orgtransaction__transaction__process_id=3,
                                                    orgtransaction__transaction__license__date_issued__year=year,
                                                    orgtransaction__transaction__license__date_issued__month__range=(
                                                        row[0], row[1])).count()

                        inactive = Org.objects.filter(org_type=t, barangay__city_code__prov_code__status=1,
                                                      orgtransaction__transaction__status_id=5,
                                                      orgtransaction__transaction__last=1,
                                                      orgtransaction__transaction__process_id=3,
                                                      orgtransaction__transaction__license__date_expired__year=year,
                                                      orgtransaction__transaction__license__date_expired__month__range=(
                                                          row[0], row[1])).count()
                        data[t.acronym]['accreditation']['active'].append(active)
                        data[t.acronym]['accreditation']['inactive'].append(inactive)

                elif t.is_worker:
                    for row in quarters:
                        active = Worker.objects.filter(org_type=t, workertransaction__transaction__status_id=4,
                                                       workertransaction__transaction__last=1,
                                                       workertransaction__transaction__process_id=3,
                                                       workertransaction__transaction__license__date_issued__year=year,
                                                       workertransaction__transaction__license__date_issued__month__range=(
                                                           row[0], row[1])).count()

                        inactive = Worker.objects.filter(org_type=t, workertransaction__transaction__status_id=5,
                                                         workertransaction__transaction__last=1,
                                                         workertransaction__transaction__process_id=3,
                                                         workertransaction__transaction__license__date_expired__year=year,
                                                         workertransaction__transaction__license__date_expired__month__range=(
                                                             row[0], row[1])).count()

                        data[t.acronym]['accreditation']['active'].append(active)
                        data[t.acronym]['accreditation']['inactive'].append(inactive)

                if t.id == 2:
                    for row in quarters:
                        active = Worker.objects.filter(org_type=t, workertransaction__transaction__status_id=4,
                                                       workertransaction__transaction__last=1,
                                                       workertransaction__transaction__process_id=3,
                                                       workertransaction__transaction__license__date_issued__year=year,
                                                       workertransaction__transaction__license__date_issued__month__range=(
                                                           row[0], row[1])).count()

                        inactive = Worker.objects.filter(org_type=t, workertransaction__transaction__status_id=5,
                                                         workertransaction__transaction__last=1,
                                                         workertransaction__transaction__process_id=3,
                                                         workertransaction__transaction__license__date_expired__year=year,
                                                         workertransaction__transaction__license__date_expired__month__range=(
                                                             row[0], row[1])).count()

                        data['cdw']['accreditation']['active'].append(active)
                        data['cdw']['accreditation']['inactive'].append(inactive)

                if t.id == 3:
                    for row in quarters:
                        active = Org.objects.filter(org_type=t, barangay__city_code__prov_code__status=1,
                                                    orgtransaction__transaction__status_id=4,
                                                    orgtransaction__transaction__last=1,
                                                    orgtransaction__transaction__process_id=1,
                                                    orgtransaction__transaction__license__date_issued__year=year,
                                                    orgtransaction__transaction__license__date_issued__month__range=(
                                                        row[0], row[1])).count()

                        inactive = Org.objects.filter(org_type=t, barangay__city_code__prov_code__status=1,
                                                      orgtransaction__transaction__status_id=5,
                                                      orgtransaction__transaction__last=1,
                                                      orgtransaction__transaction__process_id=1,
                                                      orgtransaction__transaction__license__date_expired__year=year,
                                                      orgtransaction__transaction__license__date_expired__month__range=(
                                                          row[0], row[1])).count()
                        data[t.acronym]['registration']['active'].append(active)
                        data[t.acronym]['registration']['inactive'].append(inactive)

                    for row in quarters:
                        active = Org.objects.filter(org_type=t, barangay__city_code__prov_code__status=1,
                                                    orgtransaction__transaction__status_id=4,
                                                    orgtransaction__transaction__last=1,
                                                    orgtransaction__transaction__process_id=2,
                                                    orgtransaction__transaction__license__date_issued__year=year,
                                                    orgtransaction__transaction__license__date_issued__month__range=(
                                                        row[0], row[1])).count()

                        inactive = Org.objects.filter(org_type=t, barangay__city_code__prov_code__status=1,
                                                      orgtransaction__transaction__status_id=5,
                                                      orgtransaction__transaction__last=1,
                                                      orgtransaction__transaction__process_id=2,
                                                      orgtransaction__transaction__license__date_expired__year=year,
                                                      orgtransaction__transaction__license__date_expired__month__range=(
                                                          row[0], row[1])).count()
                        data[t.acronym]['licensing']['active'].append(active)
                        data[t.acronym]['licensing']['inactive'].append(inactive)
            return data

    except Exception as e:
        print(e)


def update_sms_lib():
    try:
        with transaction.atomic():
            today = datetime.now()
            types = LibraryTypes.objects.filter(status=1).exclude(id=4).all()
            data = {
                'cso': {
                    'accreditation': {
                        'expired': 0,
                        'near': 0,
                        'contact_person': [

                        ]
                    }
                },
                'cdc': {
                    'accreditation': {
                        'expired': 0,
                        'near': 0,
                        'contact_person': [

                        ]
                    }
                },
                'cdw': {
                    'accreditation': {
                        'expired': 0,
                        'near': 0,
                        'contact_person': [

                        ]
                    }
                },
                'swda': {
                    'registration': {
                        'expired': 0,
                        'near': 0,
                        'contact_person': [

                        ]
                    },
                    'licensing': {
                        'expired': 0,
                        'near': 0,
                        'contact_person': [

                        ]
                    },
                    'accreditation': {
                        'expired': 0,
                        'near': 0,
                        'contact_person': [

                        ]
                    }
                },
                'swmcc': {
                    'accreditation': {
                        'expired': 0,
                        'near': 0,
                        'contact_person': [

                        ]
                    }
                },
                'pmc': {
                    'accreditation': {
                        'expired': 0,
                        'near': 0,
                        'contact_person': [

                        ]
                    }
                },
                'scc': {
                    'accreditation': {
                        'expired': 0,
                        'near': 0,
                        'contact_person': [

                        ]
                    }
                },
                'ps': {
                    'accreditation': {
                        'expired': 0,
                        'near': 0,
                        'contact_person': [

                        ]
                    }
                }
            }
            for row in types:
                if not row.is_worker and row.id != 3:
                    accreditation_near = Org.objects.filter(org_type=row, barangay__city_code__prov_code__status=1,
                                                            orgtransaction__transaction__last=1,
                                                            orgtransaction__transaction__process_id=3,
                                                            orgtransaction__transaction__license__date_expired__year__range=(
                                                                today.strftime("%Y"),
                                                                int(today.strftime("%Y")) + 1)).exclude(
                        Q(orgtransaction__transaction__status_id=1) | Q(orgtransaction__transaction__status_id=2) | Q(
                            orgtransaction__transaction__status_id=3)).all()
                    for i in accreditation_near:
                        if i.get_org_transaction_accreditation and i.get_org_transaction_accreditation.transaction.get_status == "near":
                            data[row.acronym]['accreditation']['near'] += 1
                            data[row.acronym]['accreditation']['contact_person'].append({
                                'status': 'near',
                                'id': i.id,
                                'cellphone_no': i.get_basic_details_cellphone
                            })
                        elif i.get_org_transaction_accreditation and i.get_org_transaction_accreditation.transaction.get_status == "expired":
                            data[row.acronym]['accreditation']['expired'] += 1
                            data[row.acronym]['accreditation']['contact_person'].append({
                                'status': 'expired',
                                'id': i.id,
                                'cellphone_no': i.get_basic_details_cellphone
                            })
                elif row.is_worker:
                    accreditation_near = Worker.objects.filter(org_type=row, workertransaction__transaction__last=1,
                                                               workertransaction__transaction__process_id=3,
                                                               workertransaction__transaction__license__date_expired__year__range=(
                                                                   today.strftime("%Y"),
                                                                   int(today.strftime("%Y")) + 1)).exclude(
                        Q(workertransaction__transaction__status_id=1) | Q(
                            workertransaction__transaction__status_id=2) | Q(
                            workertransaction__transaction__status_id=3)).all().all()
                    for i in accreditation_near:
                        if i.get_worker_transaction_accreditation.transaction.get_status == "near":
                            data[row.acronym]['accreditation']['near'] += 1
                            data[row.acronym]['accreditation']['contact_person'].append({
                                'status': 'near',
                                'id': i.id,
                                'cellphone_no': i.get_worker_detail_cellphone
                            })
                        elif i.get_worker_transaction_accreditation.transaction.get_status == "expired":
                            data[row.acronym]['accreditation']['expired'] += 1
                            data[row.acronym]['accreditation']['contact_person'].append({
                                'status': 'expired',
                                'id': i.id,
                                'cellphone_no': i.get_worker_detail_cellphone
                            })
                elif row.id == 3:
                    registration_near = Org.objects.filter(org_type=row, barangay__city_code__prov_code__status=1,
                                                           orgtransaction__transaction__last=1,
                                                           orgtransaction__transaction__process_id=1,
                                                           orgtransaction__transaction__license__date_expired__year__range=(
                                                               today.strftime("%Y"),
                                                               int(today.strftime("%Y")) + 1)).exclude(
                        Q(orgtransaction__transaction__status_id=1) | Q(
                            orgtransaction__transaction__status_id=2) | Q(
                            orgtransaction__transaction__status_id=3)).all().all()

                    license_near = Org.objects.filter(org_type=row, barangay__city_code__prov_code__status=1,
                                                      orgtransaction__transaction__last=1,
                                                      orgtransaction__transaction__process_id=2,
                                                      orgtransaction__transaction__license__date_expired__year__range=(
                                                          today.strftime("%Y"), int(today.strftime("%Y")) + 1)).exclude(
                        Q(orgtransaction__transaction__status_id=1) | Q(
                            orgtransaction__transaction__status_id=2) | Q(
                            orgtransaction__transaction__status_id=3)).all()

                    accreditation_near = Org.objects.filter(org_type=row, barangay__city_code__prov_code__status=1,
                                                            orgtransaction__transaction__last=1,
                                                            orgtransaction__transaction__process_id=3,
                                                            orgtransaction__transaction__license__date_expired__year__range=(
                                                                today.strftime("%Y"),
                                                                int(today.strftime("%Y")) + 1)).exclude(
                        Q(orgtransaction__transaction__status_id=1) | Q(
                            orgtransaction__transaction__status_id=2) | Q(
                            orgtransaction__transaction__status_id=3)).all().all()

                    for i in registration_near:
                        if i.get_org_transaction_registration.transaction.get_status == "near":
                            data[row.acronym]['registration']['near'] += 1
                            data[row.acronym]['registration']['contact_person'].append({
                                'status': 'near',
                                'id': i.id,
                                'cellphone_no': i.get_basic_details_cellphone
                            })
                        elif i.get_org_transaction_registration.transaction.get_status == "expired":
                            data[row.acronym]['registration']['expired'] += 1
                            data[row.acronym]['registration']['contact_person'].append({
                                'status': 'expired',
                                'id': i.id,
                                'cellphone_no': i.get_basic_details_cellphone
                            })
                    for i in license_near:
                        if i.get_org_transaction_license.transaction.get_status == "near":
                            data[row.acronym]['licensing']['near'] += 1
                            data[row.acronym]['licensing']['contact_person'].append({
                                'status': 'near',
                                'id': i.id,
                                'cellphone_no': i.get_basic_details_cellphone
                            })
                        elif i.get_org_transaction_license.transaction.get_status == "expired":
                            data[row.acronym]['licensing']['expired'] += 1
                            data[row.acronym]['licensing']['contact_person'].append({
                                'status': 'expired',
                                'id': i.id,
                                'cellphone_no': i.get_basic_details_cellphone
                            })
                    for i in accreditation_near:
                        if i.get_org_transaction_accreditation.transaction.get_status == "near":
                            data[row.acronym]['accreditation']['near'] += 1
                            data[row.acronym]['accreditation']['contact_person'].append({
                                'status': 'near',
                                'id': i.id,
                                'cellphone_no': i.get_basic_details_cellphone
                            })
                        elif i.get_org_transaction_accreditation.transaction.get_status == "expired":
                            data[row.acronym]['accreditation']['expired'] += 1
                            data[row.acronym]['accreditation']['contact_person'].append({
                                'status': 'expired',
                                'id': i.id,
                                'cellphone_no': i.get_basic_details_cellphone
                            })
            print(data)
            return data
    except Exception as e:
        print(e)
