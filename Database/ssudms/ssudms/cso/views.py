from django.shortcuts import render, redirect
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from frontend.forms import CSOForm, CSOOrgDetailsForm, CSOOrgContactForm, CSOOrgContactPersonForm, CSOTransactionForm
from frontend.models import Designation, Cso, PdsProvince, PdsCity, PdsBarangay, OrgType, OrgDetails, Org, Worker, \
    WorkerDetails, License, Transactions
import datetime


@login_required(login_url='/login')
@require_http_methods(['GET', 'POST'])
def csoIndexPage(request):
    try:
        if request.GET.get('province'):
            province_id = request.GET.get('province')
            province = PdsProvince.objects.get(id=province_id)
            city = serializers.serialize('json', PdsCity.objects.filter(prov_code=province).all())
            return JsonResponse({'city': city}, status=200)

        elif request.GET.get('city'):
            city_id = request.GET.get('city')
            city = PdsCity.objects.get(id=city_id)
            barangay = serializers.serialize('json', PdsBarangay.objects.filter(city_code=city.code).all())
            return JsonResponse({'barangay': barangay}, status=200)

        cso = Cso.objects.all().order_by('-id')
        p = Paginator(cso, 10)
        page = p.page(1 if request.GET.get('page_num') is None else request.GET.get('page_num'))
        data = []
        for row in page:
            transaction = Transactions.objects.filter(orgdetails__id=row.details.id, tstatus=1).first()
            if transaction:
                temp_dict = {
                    'id': row.id,
                    'name': row.details.org.name,
                    'address': row.details.pds_barangay.city_code.name,
                    'email': row.details.email,
                    'landline': row.details.landline,
                    'fax': row.details.fax,
                    'cellphone': row.details.cellphone,
                    'contact_person': '{} {} {} {}'.format(row.worker.first_name, row.worker.middle_name[
                                                                                      0] + '.' if row.worker.middle_name else '',
                                                           row.worker.last_name, row.worker.extension),
                    'designation': row.worker.designation.name,
                    'ga': row.ga,
                    'approved_program': row.approved_program,
                    'certificate': transaction.status.name,
                    'control_no': transaction.license.license_key,
                    'issued': transaction.license.date_issued,
                    'expiry': transaction.license.date_expired,
                    'transaction': 1,
                    'date_left': (transaction.license.date_expired - transaction.license.date_issued).days
                }
                data.append(temp_dict)
            else:
                temp_dict = {
                    'id': row.id,
                    'name': row.details.org.name,
                    'address': row.details.pds_barangay.city_code.name,
                    'email': row.details.email,
                    'landline': row.details.landline,
                    'fax': row.details.fax,
                    'cellphone': row.details.cellphone,
                    'contact_person': '{} {} {} {}'.format(row.worker.first_name, row.worker.middle_name[
                                                                                      0] + '.' if row.worker.middle_name else '',
                                                           row.worker.last_name, row.worker.extension),
                    'designation': row.worker.designation.name,
                    'ga': row.ga,
                    'approved_program': row.approved_program,
                    'certificate': '',
                    'control_no': '',
                    'issued': '',
                    'expiry': '',
                    'transaction': 0
                }
                data.append(temp_dict)

        context = {
            'action': 'cso',
            'data': data,
            'cso': page
        }
        return render(request, 'cso/cso.html', context)

    except Cso.DoesNotExist as e:
        print(e)
        return redirect('cso-index-page')

    except Org.DoesNotExist as e:
        print(e)
        return redirect('cso-index-page')

    except PdsBarangay.DoesNotExist as e:
        return JsonResponse({'statusMsg': str(e)}, status=404)

    except Worker.DoesNotExist as e:
        print(e)
        return redirect('cso-index-page')

    except Transactions.DoesNotExist as e:
        print(e)
        return redirect('cso-index-page')

    except Exception as e:
        print(e)
        return redirect('cso-index-page')


@login_required(login_url='/login')
@require_http_methods(['GET', 'POST'])
def csoAddPage(request):
    try:
        if not request.GET.get('action') and not request.GET.get('cso_id'):
            if request.method == "POST":
                form = CSOForm(request.POST)
                if form.is_valid():
                    org_name = form.cleaned_data['org_name']
                    barangay_id = request.POST.get('barangay')
                    email = form.cleaned_data['email']
                    landline = form.cleaned_data['landline']
                    fax = form.cleaned_data['fax']
                    cellphone = form.cleaned_data['cellphone']
                    first_name = form.cleaned_data['first_name']
                    middle_name = form.cleaned_data['middle_name']
                    last_name = form.cleaned_data['last_name']
                    extension = form.cleaned_data['extension']
                    designation = form.cleaned_data['designation']
                    ga = form.cleaned_data['ga']
                    approved_program = form.cleaned_data['approved_program']

                    barangay = PdsBarangay.objects.get(id=barangay_id)

                    org = Org(name=org_name, org_type_id=1)
                    org.save()

                    org_details = OrgDetails(pds_barangay=barangay, email=email, landline=landline, cellphone=cellphone,
                                             fax=fax, org=org, created_by=request.user)
                    org_details.save()

                    worker = Worker(first_name=''.join(i for i in first_name if i.isalnum()),
                                    middle_name=''.join(i for i in middle_name if i.isalnum()),
                                    last_name=''.join(i for i in last_name if i.isalnum()),
                                    extension=extension, designation=designation)
                    worker.save()

                    cso = Cso(ga=ga, approved_program=approved_program, details=org_details, worker=worker)
                    cso.save()

                    return JsonResponse({'statusMsg': 'Form has been successfully created.'}, status=200)

            context = {
                'form': CSOForm(),
                'action': 'add'
            }
            return render(request, 'cso/cso.html', context)

        elif request.GET.get('action') == "transaction" and request.GET.get('cso_id'):
            if request.method == "POST":
                cso_id = request.POST.get('cso_id')
                control_no = request.POST.get('control_no')
                date_issued = request.POST.get('date_issued')
                years = request.POST.get('years')

                cso = Cso.objects.get(id=cso_id)
                if cso.id == int(request.GET.get('cso_id')):
                    details = OrgDetails.objects.get(id=cso.details.id)
                    transaction = Transactions.objects.filter(orgdetails__id=cso.details.id, tstatus=1).first()
                    check_license = License.objects.filter(license_key=control_no).first()
                    if check_license is None:
                        if transaction is None:
                            license = License(date_issued=date_issued,
                                              date_expired=date_issued.replace(date_issued[0:4],
                                                                               str(int(date_issued[0:4]) + int(years))),
                                              license_key=control_no
                                              )
                            license.save()
                            transaction = Transactions(transaction_type_id=1, created_by=request.user, license=license,
                                                       status_id=1)
                            transaction.save()

                            details.transactions.add(transaction)
                            return JsonResponse({'statusMsg': 'You have successfully added a control no.'}, status=200)
                        else:
                            if transaction:
                                transaction.tstatus = 0
                                transaction.license.status = 0
                                transaction.save()

                                license = License(date_issued=date_issued,
                                                  date_expired=date_issued.replace(date_issued[0:4],
                                                                                   str(int(date_issued[0:4]) + int(
                                                                                       years))),
                                                  license_key=control_no
                                                  )
                                license.save()
                                transaction = Transactions(transaction_type_id=1, created_by=request.user,
                                                           license=license,
                                                           status_id=1)
                                transaction.save()

                                details.transactions.add(transaction)
                                return JsonResponse({'statusMsg': 'You have successfully added a control no.'}, status=200)

                    return JsonResponse({'statusMsg': 'Duplicate control number.'}, status=404)

            cso_id = request.GET.get('cso_id')
            cso = Cso.objects.get(id=cso_id)
            return JsonResponse({'cso_id': cso.id}, status=200)
    except Exception as e:
        print(e)


@login_required(login_url='/login')
@require_http_methods(['GET', 'POST'])
def csoUpdatePage(request):
    try:
        if not request.GET.get('action') and request.GET.get('cso_id'):
            cso_id = request.GET.get('cso_id')
            cso = Cso.objects.get(id=cso_id)
            org_form_data = {
                'province': cso.details.pds_barangay.city_code.prov_code.id,
                'org_name': cso.details.org.name,
                'ga': cso.ga,
                'approved_program': cso.approved_program,
                'cso': cso.id
            }

            contact_form_data = {
                'email': cso.details.email,
                'landline': cso.details.landline,
                'cellphone': cso.details.cellphone,
                'fax': cso.details.fax,
                'cso': cso.id
            }

            contact_person_form_data = {
                'first_name': cso.worker.first_name,
                'middle_name': cso.worker.middle_name,
                'last_name': cso.worker.last_name,
                'extension': cso.worker.extension,
                'designation': cso.worker.designation.id,
                'cso': cso.id
            }

            transaction_form_data = None
            transaction = Transactions.objects.filter(orgdetails__id=cso.details.id, tstatus=1).first()
            if transaction:
                transaction_form_data = {
                    'control_no': transaction.license.license_key,
                    'date_issued': transaction.license.date_issued,
                    'date_expired': transaction.license.date_expired,
                    'transaction': transaction.id,
                    'cso': cso.id,
                }

            context = {
                'form': CSOForm(),
                'org_form': CSOOrgDetailsForm(initial=org_form_data),
                'contact_form': CSOOrgContactForm(initial=contact_form_data),
                'contact_person_form': CSOOrgContactPersonForm(initial=contact_person_form_data),
                'transaction_form': CSOTransactionForm(initial=transaction_form_data) if transaction_form_data else None,
                'action': 'update',
                'cso': cso
            }
            return render(request, 'cso/cso.html', context)
        elif request.GET.get('action') == "orgdetails" and request.GET.get('cso_id') and request.method == "POST":
            today = datetime.datetime.now()
            form = CSOOrgDetailsForm(request.POST)
            if form.is_valid():
                cso_id = form.cleaned_data['cso']
                barangay_id = request.POST.get('barangay')
                org_name = form.cleaned_data['org_name']
                ga = form.cleaned_data['ga']
                approved_program = form.cleaned_data['approved_program']

                cso = Cso.objects.get(id=cso_id)
                if cso.id == int(request.GET.get('cso_id')):
                    org = Org.objects.get(id=cso.details.org.id)
                    details = OrgDetails.objects.get(id=cso.details.id)

                    cso.ga = ga
                    cso.approved_program = approved_program
                    cso.save()

                    org.name = org_name
                    org.save()

                    if barangay_id is not None:
                        barangay = PdsBarangay.objects.get(id=barangay_id)
                        details.pds_barangay = barangay
                        details.date_updated = datetime.datetime.now()
                        details.updated_by = request.user
                        details.save()

                    return JsonResponse({'statusMsg': 'Organization Details Successfully updated!'}, status=200)

                else:
                    return JsonResponse({'statusMsg': 'Unauthorized Access!'}, status=404)

        elif request.GET.get('action') == "contactdetails" and request.GET.get(
                'cso_id') and request.method == "POST":
            today = datetime.datetime.now()
            form = CSOOrgContactForm(request.POST)
            if form.is_valid():
                cso_id = form.cleaned_data['cso']
                email = form.cleaned_data['email']
                landline = form.cleaned_data['landline']
                fax = form.cleaned_data['fax']
                cellphone = form.cleaned_data['cellphone']

                cso = Cso.objects.get(id=cso_id)
                if cso.id == int(request.GET.get('cso_id')):
                    details = OrgDetails.objects.get(id=cso.details.id)
                    details.email = email
                    details.landline = landline
                    details.fax = fax
                    details.cellphone = cellphone
                    details.date_updated = datetime.datetime.now()
                    details.updated_by = request.user
                    details.save()
                    return JsonResponse({'statusMsg': 'Contact Details Successfully updated!'}, status=200)

                else:
                    return JsonResponse({'statusMsg': 'Unauthorized Access!'}, status=404)

        elif request.GET.get('action') == "contactpersondetails" and request.GET.get(
                'cso_id') and request.method == "POST":
            today = datetime.datetime.now()
            form = CSOOrgContactPersonForm(request.POST)
            if form.is_valid():
                cso_id = form.cleaned_data['cso']
                first_name = form.cleaned_data['first_name']
                middle_name = form.cleaned_data['middle_name']
                last_name = form.cleaned_data['last_name']
                extension = form.cleaned_data['extension']
                designation = form.cleaned_data['designation']

                cso = Cso.objects.get(id=cso_id)
                if cso.id == int(request.GET.get('cso_id')):
                    worker = Worker.objects.get(id=cso.worker.id)
                    details = OrgDetails.objects.get(id=cso.details.id)

                    worker.first_name = ''.join(i for i in first_name if i.isalnum())
                    worker.middle_name = ''.join(i for i in middle_name if i.isalnum())
                    worker.last_name = ''.join(i for i in last_name if i.isalnum())
                    worker.extension = extension
                    worker.designation = designation

                    worker.save()

                    details.date_updated = datetime.datetime.now()
                    details.updated_by = request.user
                    details.save()
                    return JsonResponse({'statusMsg': 'Contact Person Details Successfully updated!'}, status=200)
                else:
                    return JsonResponse({'statusMsg': 'Unauthorized Access!'}, status=404)

        elif request.GET.get('action') == "accreditation" and request.GET.get(
                'cso_id') and request.method == "POST":

            form = CSOTransactionForm(request.POST)
            if form.is_valid():
                cso_id = form.cleaned_data['cso']
                transaction = form.cleaned_data['transaction']
                status = form.cleaned_data['status']

                cso = Cso.objects.get(id=cso_id)
                if cso.id == int(request.GET.get('cso_id')):
                    transaction = Transactions.objects.get(id=transaction)
                    details = OrgDetails.objects.get(transactions=transaction, id=cso.details.id)
                    list_status = ['Active', 'Inactive']
                    if status in list_status:
                        transaction.tstatus = 1 if status == "Active" else 0
                        transaction.save()

                        details.date_updated = datetime.datetime.now()
                        details.updated_by = request.user
                        details.save()
                        return JsonResponse({'statusMsg': 'Transaction successfully updated!'}, status=200)

                    return JsonResponse({'statusMsg': 'Unauthorized Access!'}, status=404)

                return JsonResponse({'statusMsg': 'Unauthorized Access!'}, status=404)

            return JsonResponse({'statusMsg': 'Form is Invalid!'}, status=404)

    except Cso.DoesNotExist as e:
        print(e)
        return redirect('cso-index-page')

    except Org.DoesNotExist as e:
        print(e)
        return redirect('cso-index-page')

    except PdsBarangay.DoesNotExist as e:
        return JsonResponse({'statusMsg': str(e)}, status=404)

    except Worker.DoesNotExist as e:
        print(e)
        return redirect('cso-index-page')

    except Transactions.DoesNotExist as e:
        print(e)
        return redirect('cso-index-page')

    except Exception as e:
        print(e)
        return redirect('cso-index-page')
