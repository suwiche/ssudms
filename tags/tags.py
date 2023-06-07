from django import template
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db.models import Q
from frontend.models import Org, OrgTransaction, Transaction, License, OrgDetails, Worker, WorkerDetails, \
    WorkerTransaction, Logs, AccountSettings, WorkerAttribute, DetailsAttribute
from backend.models import LibraryBarangay, LibraryCitymun, LibraryProvince, LibraryProcess, LibraryStatus, \
    LibraryProcessTypes, LibraryLevel, LibraryServices, LibraryExtensions, LibraryServiceDeliveryModes, \
    LibraryAgencyTypes
from datetime import date
import datetime
import requests


register = template.Library()


@register.simple_tag
def get_user_by(user_id):
    if user_id:
        user = User.objects.get(id=user_id)
        return '{} {}'.format(user.first_name, user.last_name)
    return ''


@register.simple_tag
def get_user_group(user_id):
    if user_id:
        user = User.objects.get(id=user_id)
        return str(user.groups.all()[0])

    return ''


@register.simple_tag
def get_settings(user_id):
    if user_id:
        user = AccountSettings.objects.get(user__id=user_id)
        if user:
            return user
        pass
    pass


@register.simple_tag
def get_address(barangay_id):
    if barangay_id:
        barangay = LibraryBarangay.objects.filter(id=barangay_id).first()
        return '{}, {}, {}'.format(barangay.name, barangay.city_code.name, barangay.city_code.prov_code.name)

    return ''


@register.simple_tag
def get_date(date_now):
    if date_now:
        return date_now
    return ''


@register.simple_tag
def get_datetime():
    return datetime.datetime.now()


@register.simple_tag
def get_years():
    years = []
    for i in range(1900, 2300):
        years.append(i)
    return years


@register.simple_tag
def get_status_icon(status):
    if status == 0:
        return mark_safe('<td class="text-center text-danger"><i class="fa fa-check-circle-o f-18"></i></td>')
    elif status == 1:
        return mark_safe('<td class="text-center text-success"><i class="fa fa-check-circle-o f-18"></i></td>')
    else:
        return mark_safe('<td class="text-center text-danger"></td>')


@register.simple_tag
def get_program_url_name(acronym):
    if acronym:
        return 'frontend-{}'.format(acronym)

    return ''


@register.simple_tag
def get_worker_license(transaction_id):
    if transaction_id:
        license = License.objects.filter(transaction_id=transaction_id).first()
        if license:
            return license
        return ''
    return ''


@register.simple_tag
def get_transaction(org_id, process_id):
    if org_id and process_id:
        org_transaction = OrgTransaction.objects.filter(org_id=org_id, transaction__process_id=process_id).last()
        if org_transaction:
            return org_transaction
        return ''
    return ''


@register.simple_tag
def get_worker_transaction(worker_id):
    if worker_id:
        worker_transaction = WorkerTransaction.objects.filter(worker_id=worker_id).last()
        if worker_transaction:
            return worker_transaction
        return ''
    return ''


@register.simple_tag
def get_color(license_id):
    if license_id:
        license = License.objects.filter(id=license_id).first()
        if license:
            today = date.today()
            date_left = (license.date_expired - today).days
            if date_left >= 90 and license.transaction.status.id != 5:
                return 'success'
            elif 0 < date_left < 90 and license.transaction.status.id != 5:
                return 'warning'
            else:
                return 'danger'
        pass
    return ''


@register.simple_tag
def get_details_attribute(org_id, attribute_id):
    if org_id and attribute_id:
        data = OrgDetails.objects.filter(org_id=org_id, details_attribute_id=attribute_id).first()
        return data if data else ''
    return ''


@register.simple_tag
def get_basic_details_by_name(name, type_id, org_id):
    details_attribute = DetailsAttribute.objects.filter(type_id=type_id, name__icontains=name).first()
    if details_attribute:
        basic_details = OrgDetails.objects.filter(details_attribute=details_attribute, org_id=org_id).first()
        if basic_details:
            return basic_details.values
        pass
    return ''


@register.simple_tag
def get_workers_attribute(worker_id, attribute_id):
    if worker_id and attribute_id:
        data = WorkerDetails.objects.filter(worker_id=worker_id, worker_attribute_id=attribute_id).last()
        return data
    return ''


@register.simple_tag
def get_worker_details_by_name(name, type_id, worker_id):
    worker_attribute = WorkerAttribute.objects.filter(type_id=type_id, name__icontains=name).first()
    if worker_attribute:
        worker_details = WorkerDetails.objects.filter(worker_attribute=worker_attribute, worker_id=worker_id).first()
        return worker_details.values
    return ''


@register.simple_tag
def get_workers(org_id):
    if org_id:
        data = Worker.objects.filter(org_id=org_id).all()
        return data
    return ''


@register.simple_tag
def get_transaction_types(org_type_id):
    if org_type_id:
        # 1 = Registration , 6 = License , 7 = Accreditation
        if org_type_id == 1 or org_type_id == 2 or org_type_id == 5 or org_type_id == 6 or org_type_id == 7 or org_type_id == 8:
            return [3]
        elif org_type_id == 3:
            return [1, 2, 3]


@register.simple_tag
def get_logs():
    return Logs.objects.all().order_by('-id')[:10:1]


@register.simple_tag
def get_transaction_total(org_type_id, process_id, status_id):
    if org_type_id and process_id and status_id:
        org = Org.objects.filter(org_type_id=org_type_id).all()
        counter = 0
        for row in org:
            transaction = OrgTransaction.objects.filter(org=row, transaction__status_id=status_id,
                                                        transaction__process_id=process_id).last()
            if transaction:
                counter += 1
            pass
        return counter


@register.simple_tag
def get_worker_total_accredited(org_type_id, process_id):
    if org_type_id and process_id:
        worker = Worker.objects.filter(org__org_type_id=org_type_id).all()
        counter = 0
        for row in worker:
            transaction = WorkerTransaction.objects.filter(worker=row, transaction__status_id=3,
                                                           transaction__process_id=process_id).last()
            if transaction:
                counter += 1
            pass
        return counter


@register.simple_tag
def get_worker_total_expired(org_type_id, process_id):
    if org_type_id and process_id:
        worker = Worker.objects.filter(org__org_type_id=org_type_id).all()
        counter = 0
        for row in worker:
            transaction = WorkerTransaction.objects.filter(worker=row, transaction__status_id=4,
                                                           transaction__process_id=process_id).last()
            if transaction:
                counter += 1
            pass
        return counter


@register.simple_tag
def get_org_total_registered(org_type_id):
    if org_type_id:
        return Org.objects.filter(org_type_id=org_type_id).count()


@register.simple_tag
def get_worker_total_registered(org_type_id):
    if org_type_id:
        return Worker.objects.filter(org__org_type_id=org_type_id).count()


@register.simple_tag
def api_employee_list():
    try:
        token_auth = 'Token 94f1eabd887dee4ace64ab417df3413a98d9a6c9'
        headers = {"Authorization": token_auth}

        response = requests.get("https://caraga-portal.dswd.gov.ph/api/employee/list/search/?q=Standards Section",
                                headers=headers)
        response_data = response.json()

        return response_data
    except Exception as e:
        return None


@register.simple_tag
def get_emp_pic(username):
    try:
        if username:
            token_auth = 'Token 94f1eabd887dee4ace64ab417df3413a98d9a6c9'
            headers = {"Authorization": token_auth}
            user = ''
            response = requests.get(
                "https://caraga-portal.dswd.gov.ph/api/employee/list/search/?q={}".format(username),
                headers=headers, verify=False)
            response_data = response.json()

            for i in response_data:
                if i['username'] == username:
                    user = i
                    break
            return user
    except Exception as e:
        print(e)


@register.simple_tag
def get_provinces():
    return LibraryProvince.objects.filter(status=1).all()


@register.simple_tag
def get_cities(prov_code):
    if prov_code:
        return LibraryCitymun.objects.filter(prov_code=prov_code, status=1).all()
    return LibraryCitymun.objects.filter(status=1).all()


@register.simple_tag
def get_barangays(city_code):
    if city_code:
        return LibraryBarangay.objects.filter(city_code=city_code.code, status=1).all()
    return LibraryBarangay.objects.filter(status=1).all(),


@register.simple_tag
def get_process(pk=None):
    if pk is None:
        return LibraryProcess.objects.filter(status=1).all()
    return LibraryProcess.objects.filter(id=pk, status=1).first()


@register.simple_tag
def get_status(pk=None):
    if pk is None:
        return LibraryStatus.objects.filter(status=1).all()
    return LibraryStatus.objects.filter(id=pk, status=1).first()


@register.simple_tag
def get_levels(pk=None):
    if pk is None:
        return LibraryLevel.objects.filter(status=1).all()
    return LibraryLevel.objects.filter(id=pk, status=1).first()


@register.simple_tag
def get_services(pk=None):
    if pk is None:
        return LibraryServices.objects.filter(status=1).all()
    return LibraryServices.objects.filter(id=pk, status=1).first()


@register.simple_tag
def get_service_delivery_modes(pk=None):
    if pk is None:
        return LibraryServiceDeliveryModes.objects.filter(status=1).all()
    return LibraryServiceDeliveryModes.objects.filter(id=pk, status=1).first()


@register.simple_tag
def get_agency_types(pk=None):
    if pk is None:
        return LibraryAgencyTypes.objects.filter(status=1).all()
    return LibraryAgencyTypes.objects.filter(id=pk, status=1).first()


@register.simple_tag
def get_extensions(pk=None):
    if pk is None:
        return LibraryExtensions.objects.filter(status=1).all()
    return LibraryExtensions.objects.filter(id=pk, status=1).first()


@register.simple_tag
def get_process_types(pk=None):
    if pk is None:
        return LibraryProcessTypes.objects.filter(status=1).all()
    return LibraryProcessTypes.objects.filter(id=pk, status=1).first()


@register.simple_tag
def get_worker_fullname(worker_id):
    if worker_id:
        worker = Worker.objects.filter(id=worker_id).first()
        if worker:
            return '{} {}{} {} '.format(worker.first_name, worker.middle_name if worker.middle_name else '',
                                        worker.last_name, worker.extension.name if worker.extension else '')
    return ''


@register.simple_tag
def get_total_cities():
    counter = 0
    for row in LibraryProvince.objects.filter(status=1).all():
        cities_count = LibraryCitymun.objects.filter(prov_code_id=row.id).count()
        counter = counter + cities_count

    return counter


@register.simple_tag
def get_total_barangays(prov_code=None):
    if prov_code is None:
        counter = 0
        for row in LibraryProvince.objects.filter(status=1).all():
            for i in LibraryCitymun.objects.filter(prov_code_id=row.id).all():
                brgy_counter = LibraryBarangay.objects.filter(city_code=i.code).count()
                counter = counter + brgy_counter

        return counter

    return LibraryBarangay.objects.filter(city_code__prov_code=prov_code).count()


@register.simple_tag
def get_cdc_far_to_expire(year, type_id, prov_id):
    if year and type_id and prov_id:
        counter = 0
        data = Org.objects.filter(org_type=type_id, barangay__city_code__prov_code__id=prov_id,
                                  orgtransaction__transaction__status_id=4,
                                  orgtransaction__transaction__last=1,
                                  orgtransaction__transaction__process_id=3,
                                  orgtransaction__transaction__license__date_issued__year=year).all()
        for row in data:
            if row.get_org_transaction_accreditation.transaction.get_color == "success":
                counter = counter + 1
        return counter


@register.simple_tag
def get_cdc_near_to_expire(year, type_id, prov_id):
    if year and type_id and prov_id:
        counter = 0
        data = Org.objects.filter(org_type=type_id, barangay__city_code__prov_code__id=prov_id,
                                  orgtransaction__transaction__status_id=4,
                                  orgtransaction__transaction__last=1,
                                  orgtransaction__transaction__process_id=3,
                                  orgtransaction__transaction__license__date_issued__year=year).all()
        for row in data:
            if row.get_org_transaction_accreditation.transaction.get_color == "warning":
                counter = counter + 1
        return counter


@register.simple_tag
def get_cdc_not_yet(year, type_id, prov_id):
    if year and type_id and prov_id:
        counter = Org.objects.filter(orgtransaction__transaction__last=1,
                                     orgtransaction__transaction__status_id=1,
                                     org_type=type_id, barangay__city_code__prov_code__id=prov_id,
                                     orgtransaction__transaction__process_id=3,
                                     orgtransaction__transaction__date_created__year=year).count()
        return counter


@register.simple_tag
def get_cdc_for_re_assessment(year, type_id, prov_id):
    if year and type_id and prov_id:
        counter = Org.objects.filter(
            Q(orgtransaction__transaction__status_id=2) | Q(orgtransaction__transaction__status_id=3),
            orgtransaction__transaction__last=1,
            org_type=type_id, barangay__city_code__prov_code__id=prov_id,
            orgtransaction__transaction__process_id=3,
            orgtransaction__transaction__date_created__year=year).count()
        return counter


@register.simple_tag
def get_cdc_expired(year, type_id, prov_id):
    if year and type_id and prov_id:
        counter = 0
        data = Org.objects.filter(
            Q(orgtransaction__transaction__status_id=4) | Q(orgtransaction__transaction__status_id=5) |
            Q(orgtransaction__transaction__last=1) | Q(orgtransaction__transaction__last=0) |
            Q(orgtransaction__transaction__license__date_expired__year=year) |
            Q(orgtransaction__transaction__license__date_issued__year=year), org_type=type_id,
            barangay__city_code__prov_code__id=prov_id, orgtransaction__transaction__process_id=3).all()
        for row in data:
            if row.get_org_transaction_accreditation.transaction.get_color == "danger":
                counter = counter + 1
        return counter


@register.simple_tag
def get_cdc_far_to_expire_total(year, type_id):
    if year and type_id:
        counter = 0
        data = Org.objects.filter(org_type=type_id, barangay__city_code__prov_code__status=1,
                                  orgtransaction__transaction__status_id=4,
                                  orgtransaction__transaction__last=1,
                                  orgtransaction__transaction__process_id=3,
                                  orgtransaction__transaction__license__date_issued__year=year).all()
        for row in data:
            if row.get_org_transaction_accreditation.transaction.get_color == "success":
                counter = counter + 1
        return counter


@register.simple_tag
def get_cdc_near_to_expire_total(year, type_id):
    if year and type_id:
        counter = 0
        data = Org.objects.filter(org_type=type_id, barangay__city_code__prov_code__status=1,
                                  orgtransaction__transaction__status_id=4,
                                  orgtransaction__transaction__last=1,
                                  orgtransaction__transaction__process_id=3,
                                  orgtransaction__transaction__license__date_issued__year=year).all()
        for row in data:
            if row.get_org_transaction_accreditation.transaction.get_color == "warning":
                counter = counter + 1
        return counter


@register.simple_tag
def get_cdc_not_yet_total(year, type_id):
    if year and type_id:
        counter = Org.objects.filter(orgtransaction__transaction__last=1,
                                     orgtransaction__transaction__status_id=1,
                                     org_type=type_id, barangay__city_code__prov_code__status=1,
                                     orgtransaction__transaction__process_id=3,
                                     orgtransaction__transaction__date_created__year=year).count()
        return counter


@register.simple_tag
def get_cdc_for_re_assessment_total(year, type_id):
    if year and type_id:
        counter = Org.objects.filter(
            Q(orgtransaction__transaction__status_id=2) | Q(orgtransaction__transaction__status_id=3),
            orgtransaction__transaction__last=1,
            org_type=type_id, barangay__city_code__prov_code__status=1,
            orgtransaction__transaction__process_id=3,
            orgtransaction__transaction__date_created__year=year).count()
        return counter


@register.simple_tag
def get_cdc_expired_total(year, type_id):
    if year and type_id:
        counter = 0
        data = Org.objects.filter(
            Q(orgtransaction__transaction__status_id=4) | Q(orgtransaction__transaction__status_id=5) |
            Q(orgtransaction__transaction__last=1) | Q(orgtransaction__transaction__last=0) |
            Q(orgtransaction__transaction__license__date_expired__year=year) |
            Q(orgtransaction__transaction__license__date_issued__year=year), org_type=type_id,
            barangay__city_code__prov_code__status=1, orgtransaction__transaction__process_id=3).all()
        for row in data:
            if row.get_org_transaction_accreditation.transaction.get_color == "danger":
                counter = counter + 1
        return counter


@register.simple_tag
def get_prov_org_total(year, type_id, prov_id):
    if year and type_id and prov_id:
        return Org.objects.filter(org_type_id=type_id, barangay__city_code__prov_code__id=prov_id,
                                  date_created__year=year).count()


@register.simple_tag
def get_org_total(year, type_id):
    if year and type_id:
        return Org.objects.filter(org_type_id=type_id, barangay__city_code__prov_code__status=1,
                                  date_created__year=year).count()


@register.simple_tag
def get_cdw_far_to_expire(year, type_id, prov_id):
    if year and type_id and prov_id:
        counter = 0
        data = Worker.objects.filter(org__org_type=type_id, org__barangay__city_code__prov_code__id=prov_id,
                                     workertransaction__transaction__status_id=4,
                                     workertransaction__transaction__last=1,
                                     workertransaction__transaction__process_id=3,
                                     workertransaction__transaction__license__date_issued__year=year).all()
        for row in data:
            if row.get_worker_transaction_accreditation.transaction.get_color == "success":
                counter = counter + 1
        return counter


@register.simple_tag
def get_cdw_near_to_expire(year, type_id, prov_id):
    if year and type_id and prov_id:
        counter = 0
        data = Worker.objects.filter(org__org_type=type_id, org__barangay__city_code__prov_code__id=prov_id,
                                     workertransaction__transaction__status_id=4,
                                     workertransaction__transaction__last=1,
                                     workertransaction__transaction__process_id=3,
                                     workertransaction__transaction__license__date_issued__year=year).all()
        for row in data:
            if row.get_worker_transaction_accreditation.transaction.get_color == "warning":
                counter = counter + 1
        return counter


@register.simple_tag
def get_cdw_not_yet(year, type_id, prov_id):
    if year and type_id and prov_id:
        counter = Worker.objects.filter(workertransaction__transaction__last=1,
                                        workertransaction__transaction__status_id=1,
                                        org__org_type=type_id, org__barangay__city_code__prov_code__id=prov_id,
                                        workertransaction__transaction__process_id=3,
                                        workertransaction__transaction__date_created__year=year).count()
        return counter


@register.simple_tag
def get_cdw_for_re_assessment(year, type_id, prov_id):
    if year and type_id and prov_id:
        counter = Worker.objects.filter(
            Q(workertransaction__transaction__status_id=2) | Q(workertransaction__transaction__status_id=3),
            workertransaction__transaction__last=1,
            org__org_type=type_id, org__barangay__city_code__prov_code__id=prov_id,
            workertransaction__transaction__process_id=3,
            workertransaction__transaction__date_created__year=year).count()
        return counter


@register.simple_tag
def get_cdw_expired(year, type_id, prov_id):
    if year and type_id and prov_id:
        counter = 0
        data = Worker.objects.filter(
            Q(workertransaction__transaction__status_id=4) | Q(workertransaction__transaction__status_id=5) |
            Q(workertransaction__transaction__last=1) | Q(workertransaction__transaction__last=0) |
            Q(workertransaction__transaction__license__date_expired__year=year),
            Q(workertransaction__transaction__license__date_issued__year=year),
            org__org_type=type_id, org__barangay__city_code__prov_code__id=prov_id,
            workertransaction__transaction__process_id=3).all()
        for row in data:
            if row.get_worker_transaction_accreditation.transaction.get_color == "danger":
                counter = counter + 1
        return counter


@register.simple_tag
def get_cdw_far_to_expire_total(year, type_id):
    if year and type_id:
        counter = 0
        data = Worker.objects.filter(org__org_type=type_id, org__barangay__city_code__prov_code__status=1,
                                     workertransaction__transaction__status_id=4,
                                     workertransaction__transaction__last=1,
                                     workertransaction__transaction__process_id=3,
                                     workertransaction__transaction__license__date_issued__year=year).all()
        for row in data:
            if row.get_worker_transaction_accreditation.transaction.get_color == "success":
                counter = counter + 1
        return counter


@register.simple_tag
def get_cdw_near_to_expire_total(year, type_id):
    if year and type_id:
        counter = 0
        data = Worker.objects.filter(org__org_type=type_id, org__barangay__city_code__prov_code__status=1,
                                     workertransaction__transaction__status_id=4,
                                     workertransaction__transaction__last=1,
                                     workertransaction__transaction__process_id=3,
                                     workertransaction__transaction__license__date_issued__year=year).all()
        for row in data:
            if row.get_worker_transaction_accreditation.transaction.get_color == "warning":
                counter = counter + 1
        return counter


@register.simple_tag
def get_cdw_not_yet_total(year, type_id):
    if year and type_id:
        counter = Worker.objects.filter(workertransaction__transaction__last=1,
                                        workertransaction__transaction__status_id=1,
                                        org__org_type=type_id, org__barangay__city_code__prov_code__status=1,
                                        workertransaction__transaction__process_id=3,
                                        workertransaction__transaction__date_created__year=year).count()
        return counter


@register.simple_tag
def get_cdw_for_re_assessment_total(year, type_id):
    if year and type_id:
        counter = Worker.objects.filter(
            Q(workertransaction__transaction__status_id=2) | Q(workertransaction__transaction__status_id=3),
            workertransaction__transaction__last=1,
            org__org_type=type_id, org__barangay__city_code__prov_code__status=1,
            workertransaction__transaction__process_id=3,
            workertransaction__transaction__date_created__year=year).count()
        return counter


@register.simple_tag
def get_cdw_expired_total(year, type_id):
    if year and type_id:
        counter = 0
        data = Worker.objects.filter(
            Q(workertransaction__transaction__status_id=4) | Q(workertransaction__transaction__status_id=5) |
            Q(workertransaction__transaction__last=1) | Q(workertransaction__transaction__last=0) |
            Q(workertransaction__transaction__license__date_expired__year=year) |
            Q(workertransaction__transaction__license__date_issued__year=year),
            org__org_type=type_id, org__barangay__city_code__prov_code__status=1,
            workertransaction__transaction__process_id=3).all()
        for row in data:
            if row.get_worker_transaction_accreditation.transaction.get_color == "danger":
                counter = counter + 1
        return counter


@register.simple_tag
def get_prov_worker_total(year, type_id, prov_id):
    if year and type_id and prov_id:
        return Worker.objects.filter(org__org_type_id=type_id, org__barangay__city_code__prov_code__id=prov_id,
                                     org__date_created__year=year).count()


@register.simple_tag
def get_worker_total(year, type_id):
    if year and type_id:
        return Worker.objects.filter(org__org_type_id=type_id, org__barangay__city_code__prov_code__status=1,
                                     org__date_created__year=year).count()


@register.simple_tag
def get_cdccdw_total(year, type_id):
    if year and type_id:
        return get_worker_total(year, type_id) + get_org_total(year, type_id)


@register.simple_tag
def get_prov_cdccdw_total(year, type_id, prov_id):
    if year and type_id and prov_id:
        return get_prov_worker_total(year, type_id, prov_id) + get_prov_org_total(year, type_id, prov_id)

