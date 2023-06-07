from django.contrib.auth.models import User
from django.db import models


class PdsProvince(models.Model):
    name = models.CharField(max_length=64)
    status = models.IntegerField()
    upload_by_id = models.IntegerField()

    class Meta:
        db_table = 'pds_province'

    def __str__(self):
        return '{}'.format(self.name)


class PdsCity(models.Model):
    name = models.CharField(max_length=64, unique=True)
    code = models.IntegerField(unique=True)
    prov_code = models.ForeignKey(PdsProvince, on_delete=models.RESTRICT)
    status = models.IntegerField()
    upload_by_id = models.IntegerField()

    class Meta:
        db_table = 'pds_city'


class PdsBarangay(models.Model):
    name = models.CharField(max_length=128)
    city_code = models.ForeignKey(PdsCity, to_field='code', on_delete=models.RESTRICT)
    status = models.IntegerField()
    upload_by_id = models.IntegerField()

    class Meta:
        db_table = 'pds_barangay'


class Docs(models.Model):
    date_completed_docs = models.DateField()
    date_of_assessment = models.DateField()


class Category(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='updated_by_category')
    status = models.IntegerField(default=1)


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='updated_by_subcategory')
    status = models.IntegerField(default=1)


class Designation(models.Model):
    name = models.CharField(max_length=20)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True, blank=False)
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.RESTRICT,
                                   related_name='updated_by_designation')
    status = models.IntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.name)


class WorkerDetails(models.Model):
    pds_barangay = models.ForeignKey(PdsBarangay, null=True, on_delete=models.RESTRICT)
    email = models.CharField(max_length=40)
    landline = models.CharField(max_length=15)
    cellphone = models.CharField(max_length=15)
    fax = models.CharField(max_length=15)


class Worker(models.Model):
    EXTENSION_CHOICES = [
        ('', 'None'),
        ('Jr.', 'Jr.'),
        ('Jr', 'Sr.'),
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III')
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Rather_not_to_say', 'Rather not to say')
    ]
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30)
    extension = models.CharField(max_length=10, null=True, blank=True, choices=EXTENSION_CHOICES)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    designation = models.ForeignKey(Designation, on_delete=models.RESTRICT)
    details = models.ForeignKey(WorkerDetails, null=True, on_delete=models.RESTRICT)


class License(models.Model):
    date_issued = models.DateField(null=True)
    date_expired = models.DateField(null=True)
    license_key = models.CharField(max_length=50)
    status = models.IntegerField(default=1)


class Status(models.Model):
    name = models.CharField(max_length=15)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, related_name='status_updated', on_delete=models.RESTRICT)
    status = models.IntegerField(default=1)


class Level(models.Model):
    level = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, related_name='level_updated', on_delete=models.RESTRICT)
    status = models.IntegerField(default=1)


class OrgType(models.Model):
    name = models.CharField(max_length=10)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='org_type_updated', on_delete=models.RESTRICT)
    status = models.IntegerField(default=1)


class Org(models.Model):
    name = models.CharField(max_length=50)
    org_type = models.ForeignKey(OrgType, on_delete=models.RESTRICT)


class TransactionType(models.Model):
    name = models.CharField(max_length=15)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, related_name='transaction_type_updated', on_delete=models.RESTRICT)
    status = models.IntegerField(default=1)


class Transactions(models.Model):
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.RESTRICT)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    status = models.ForeignKey(Status, null=True, on_delete=models.RESTRICT)
    level = models.ForeignKey(Level, null=True, on_delete=models.RESTRICT)
    license = models.ForeignKey(License, on_delete=models.RESTRICT)
    tstatus = models.IntegerField(default=1)


class OrgDetails(models.Model):
    pds_barangay = models.ForeignKey(PdsBarangay, null=True, on_delete=models.RESTRICT)
    email = models.CharField(max_length=40)
    landline = models.CharField(max_length=15)
    cellphone = models.CharField(max_length=15)
    fax = models.CharField(max_length=15)
    org = models.ForeignKey(Org, on_delete=models.RESTRICT)
    transactions = models.ManyToManyField(Transactions)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True, blank=False)
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.RESTRICT,
                                   related_name='updated_by_org_details')


class Cdw(models.Model):
    docs = models.ForeignKey(Docs, on_delete=models.RESTRICT, null=True)
    worker = models.ForeignKey(Worker, on_delete=models.RESTRICT)
    details = models.ForeignKey(OrgDetails, on_delete=models.RESTRICT)


class Cso(models.Model):
    ga = models.CharField(max_length=20)
    approved_program = models.CharField(max_length=100)
    details = models.ForeignKey(OrgDetails, on_delete=models.RESTRICT)
    worker = models.ForeignKey(Worker, on_delete=models.RESTRICT)


class Cdc(models.Model):
    details = models.ForeignKey(OrgDetails, on_delete=models.RESTRICT)
    workers = models.ManyToManyField(Cdw)


class Swda(models.Model):
    workers = models.ManyToManyField(Worker)
    details = models.ForeignKey(OrgDetails, on_delete=models.RESTRICT)
    services = models.CharField(max_length=255)
    clientele = models.CharField(max_length=50)
    service_delivery_mode = models.CharField(max_length=50)
    area_operation = models.CharField(max_length=50)
    remarks = models.CharField(max_length=50)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.RESTRICT)
    classification = models.CharField(max_length=20)
