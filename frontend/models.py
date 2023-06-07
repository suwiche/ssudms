from django.db import models
from django.db.models import Q

from backend.models import LibraryBarangay, DetailsAttribute, LibraryServices, LibraryProcess, LibraryStatus, \
    LibraryExtensions, LibraryTypes, WorkerAttribute, LibraryLevel, LibraryProcessTypes, LibraryServiceDeliveryModes, \
    LibraryAgencyTypes
from django.contrib.auth.models import User
from datetime import date


class AccountSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    theme = models.CharField(max_length=20, default=0)
    id_number = models.CharField(max_length=20)


class Org(models.Model):
    name = models.CharField(max_length=100)
    barangay = models.ForeignKey(LibraryBarangay, null=True, on_delete=models.DO_NOTHING)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='org_updated', on_delete=models.RESTRICT)
    org_type = models.ForeignKey(LibraryTypes, models.RESTRICT)
    agency_type = models.ForeignKey(LibraryAgencyTypes, null=True, on_delete=models.RESTRICT)

    @property
    def get_org_transaction_registration(self):
        return OrgTransaction.objects.filter(org_id=self.id, transaction__last=1, transaction__process_id=1).last()

    @property
    def get_org_transaction_license(self):
        return OrgTransaction.objects.filter(org_id=self.id, transaction__last=1, transaction__process_id=2).last()

    @property
    def get_org_transaction_accreditation(self):
        return OrgTransaction.objects.filter(org_id=self.id, transaction__last=1, transaction__process_id=3).last()

    @property
    def get_all_process_org_transaction(self):
        return OrgTransaction.objects.filter(org_id=self.id, transaction__last=1).all()

    @property
    def get_workers(self):
        return Worker.objects.filter(Q(org_id=self.id)).all()

    @property
    def get_province(self):
        return self.barangay.city_code.prov_code.name

    @property
    def get_city(self):
        return self.barangay.city_code.name

    @property
    def get_barangay(self):
        return self.barangay.name

    @property
    def get_org_service(self):
        return OrgService.objects.filter(org_id=self.id).first()

    @property
    def get_address(self):
        return '{}, {}, {}'.format(self.barangay.name, self.barangay.city_code.name, self.barangay.city_code.prov_code.name)

    @property
    def get_worker_count(self):
        return Worker.objects.filter(org_id=self.id).count()

    @property
    def get_check_if_renewal_r(self):
        return OrgTransaction.objects.filter(Q(transaction__status_id=4) | Q(transaction__status_id=5),
                                             org_id=self.id, transaction__process_id=1, transaction__last=0).count()

    @property
    def get_check_if_renewal_l(self):
        return OrgTransaction.objects.filter(Q(transaction__status_id=4) | Q(transaction__status_id=5),
                                             org_id=self.id, transaction__process_id=2, transaction__last=0).count()

    @property
    def get_check_if_renewal_a(self):
        return OrgTransaction.objects.filter(Q(transaction__status_id=4) | Q(transaction__status_id=5),
                                             org_id=self.id, transaction__process_id=3, transaction__last=0).count()

    @property
    def get_basic_details_cellphone(self):
        details_attribute = DetailsAttribute.objects.filter(type=self.org_type, name__icontains='Cellphone').first()
        if details_attribute:
            basic_details = OrgDetails.objects.filter(details_attribute=details_attribute, org_id=self.id).first()
            if basic_details:
                return basic_details.values
            pass
        return ''

    @property
    def get_first_worker(self):
        worker = Worker.objects.filter(org_id=self.id).first()
        return worker

    @property
    def get_all_worker_except_first(self):
        worker = Worker.objects.filter(org_id=self.id).all()
        [0, 1, 2, 3]
        print(worker[1:])
        return worker[1:]


class OrgDetails(models.Model):
    details_attribute = models.ForeignKey(DetailsAttribute, on_delete=models.RESTRICT)
    values = models.TextField(null=True)
    org = models.ForeignKey(Org, models.RESTRICT)


class OrgService(models.Model):
    org = models.ForeignKey(Org, models.RESTRICT)
    service = models.ForeignKey(LibraryServices, null=True, on_delete=models.RESTRICT)
    service_delivery_mode = models.ForeignKey(LibraryServiceDeliveryModes, null=True, on_delete=models.RESTRICT)


class WorkerDetails(models.Model):
    worker_attribute = models.ForeignKey(WorkerAttribute, models.RESTRICT)
    values = models.TextField(null=True)
    worker = models.ForeignKey('Worker', models.RESTRICT)


class Transaction(models.Model):
    date_received = models.DateField(auto_now_add=False, null=True)
    date_complete_docs = models.DateField(auto_now_add=False, null=True)
    date_assessed = models.DateField(auto_now_add=False, null=True)
    date_endorsed = models.DateField(auto_now_add=False, null=True)
    date_returned = models.DateField(auto_now_add=False, null=True)
    assessed_by = models.CharField(null=True, max_length=50)
    process = models.ForeignKey(LibraryProcess, models.RESTRICT)
    status = models.ForeignKey(LibraryStatus, models.RESTRICT)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='transaction_updated', on_delete=models.RESTRICT)
    last = models.IntegerField()
    process_type = models.ForeignKey(LibraryProcessTypes, null=True, on_delete=models.RESTRICT)
    remarks = models.CharField(null=True, max_length=100)

    @property
    def get_license(self):
        return License.objects.filter(transaction_id=self.id).first()

    @property
    def get_color(self):
        license = License.objects.filter(transaction_id=self.id).first()
        if license:
            today = date.today()
            date_left = (license.date_expired - today).days
            if date_left >= 90 and license.transaction.status.id != 5:
                return 'success'
            elif 0 < date_left < 90 and license.transaction.status.id != 5:
                return 'warning'
            else:
                return 'danger'

    @property
    def get_status(self):
        license = License.objects.filter(transaction_id=self.id).first()
        if license:
            today = date.today()
            date_left = (license.date_expired - today).days
            if date_left >= 90 and license.transaction.status.id != 5:
                return 'far'
            elif 0 < date_left < 90 and license.transaction.status.id != 5:
                return 'near'
            elif date_left < 0 and license.transaction.status.id != 5:
                return 'expired'
            elif license.transaction.status.id == 5:
                return 'inactive'


class OrgTransaction(models.Model):
    transaction = models.ForeignKey('Transaction', models.RESTRICT)
    org = models.ForeignKey(Org, models.RESTRICT)


class Worker(models.Model):
    SEX_CHOICES = [
        ('1', 'Male'),
        ('0', 'Female'),
        ('2', 'N/A')
    ]
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    extension = models.ForeignKey(LibraryExtensions, null=True, on_delete=models.RESTRICT)
    date_of_birth = models.DateField(auto_now_add=False, null=True)
    sex = models.IntegerField(default=2)
    org = models.ForeignKey(Org, null=True, on_delete=models.RESTRICT)
    org_type = models.ForeignKey(LibraryTypes, null=True, on_delete=models.RESTRICT)
    address = models.CharField(max_length=255, null=True)
    province = models.CharField(max_length=100, null=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.RESTRICT)

    @property
    def get_worker_transaction_accreditation(self):
        return WorkerTransaction.objects.filter(worker_id=self.id, transaction__last=1,
                                                transaction__process_id=3).last()

    @property
    def get_worker_fullname(self):
        return '{} {}{}{}'.format(self.first_name, self.middle_name + '. ' if self.middle_name else '', self.last_name,
                                  ' '+self.extension.name + ',' if self.extension else '')

    @property
    def get_worker_detail_cellphone(self):
        worker_attribute = WorkerAttribute.objects.filter(type=self.org_type, name__icontains='Cellphone').first()
        if worker_attribute:
            worker_details = WorkerDetails.objects.filter(worker_attribute=worker_attribute,
                                                          worker_id=self.id).first()
            return worker_details.values
        return ''

    @property
    def get_check_if_renewal(self):
        return WorkerTransaction.objects.filter(worker_id=self.id).count()

    @property
    def get_sex(self):
        if self.sex == 0:
            return 'Female'
        elif self.sex == 1:
            return 'Male'
        else:
            return ''


class WorkerTransaction(models.Model):
    transaction = models.ForeignKey(Transaction, models.RESTRICT)
    worker = models.ForeignKey(Worker, models.RESTRICT)


class License(models.Model):
    number = models.CharField(max_length=50)
    date_issued = models.DateField()
    date_expired = models.DateField()
    transaction = models.ForeignKey('Transaction', models.RESTRICT)
    validity = models.IntegerField()
    level = models.ForeignKey(LibraryLevel, null=True, on_delete=models.DO_NOTHING)


class Logs(models.Model):
    ACTION_CHOICES = [
        ('Added', 'Added'),
        ('Read', 'Read'),
        ('Updated', 'Updated'),
        ('Deleted', 'Deleted')
    ]
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    created_by = models.ForeignKey(User, models.RESTRICT)
    message = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
