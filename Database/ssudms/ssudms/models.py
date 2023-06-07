# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FrontendCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    date_created = models.DateField()
    date_updated = models.DateField()
    status = models.IntegerField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING)
    updated_by = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'frontend_category'


class FrontendCdc(models.Model):
    id = models.BigAutoField(primary_key=True)
    details = models.ForeignKey('FrontendOrgdetails', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'frontend_cdc'


class FrontendCdcWorkers(models.Model):
    id = models.BigAutoField(primary_key=True)
    cdc = models.ForeignKey(FrontendCdc, models.DO_NOTHING)
    cdw = models.ForeignKey('FrontendCdw', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'frontend_cdc_workers'
        unique_together = (('cdc', 'cdw'),)


class FrontendCdw(models.Model):
    id = models.BigAutoField(primary_key=True)
    details = models.ForeignKey('FrontendOrgdetails', models.DO_NOTHING)
    worker = models.ForeignKey('FrontendWorker', models.DO_NOTHING)
    docs = models.ForeignKey('FrontendDocs', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'frontend_cdw'


class FrontendCso(models.Model):
    id = models.BigAutoField(primary_key=True)
    ga = models.CharField(max_length=20)
    approved_program = models.CharField(max_length=100)
    details = models.ForeignKey('FrontendOrgdetails', models.DO_NOTHING)
    worker = models.ForeignKey('FrontendWorker', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'frontend_cso'


class FrontendDesignation(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20)
    date_created = models.DateField()
    date_updated = models.DateField(blank=True, null=True)
    status = models.IntegerField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING)
    updated_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'frontend_designation'


class FrontendDocs(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_completed_docs = models.DateField()
    date_of_assessment = models.DateField()

    class Meta:
        managed = False
        db_table = 'frontend_docs'


class FrontendLevel(models.Model):
    id = models.BigAutoField(primary_key=True)
    level = models.IntegerField()
    date_created = models.DateField()
    date_updated = models.DateField(blank=True, null=True)
    status = models.IntegerField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING)
    updated_by = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'frontend_level'


class FrontendLicense(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_issued = models.DateField(blank=True, null=True)
    date_expired = models.DateField(blank=True, null=True)
    license_key = models.CharField(max_length=50)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'frontend_license'


class FrontendOrg(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    org_type = models.ForeignKey('FrontendOrgtype', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'frontend_org'


class FrontendOrgdetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=40)
    landline = models.CharField(max_length=15)
    cellphone = models.CharField(max_length=15)
    fax = models.CharField(max_length=15)
    org = models.ForeignKey(FrontendOrg, models.DO_NOTHING)
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    pds_barangay_id = models.BigIntegerField(blank=True, null=True)
    date_created = models.DateField()
    date_updated = models.DateField(blank=True, null=True)
    updated_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'frontend_orgdetails'


class FrontendOrgdetailsTransactions(models.Model):
    id = models.BigAutoField(primary_key=True)
    orgdetails = models.ForeignKey(FrontendOrgdetails, models.DO_NOTHING)
    transactions = models.ForeignKey('FrontendTransactions', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'frontend_orgdetails_transactions'
        unique_together = (('orgdetails', 'transactions'),)


class FrontendOrgtype(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=10)
    date_created = models.DateField()
    date_updated = models.DateField(blank=True, null=True)
    status = models.IntegerField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING)
    updated_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'frontend_orgtype'


class FrontendStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=15)
    date_created = models.DateField()
    date_updated = models.DateField(blank=True, null=True)
    status = models.IntegerField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING)
    updated_by = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'frontend_status'


class FrontendSubcategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    date_created = models.DateField()
    date_updated = models.DateField()
    status = models.IntegerField()
    category = models.ForeignKey(FrontendCategory, models.DO_NOTHING)
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING)
    updated_by = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'frontend_subcategory'


class FrontendSwda(models.Model):
    id = models.BigAutoField(primary_key=True)
    services = models.CharField(max_length=255)
    clientele = models.CharField(max_length=50)
    service_delivery_mode = models.CharField(max_length=50)
    area_operation = models.CharField(max_length=50)
    remarks = models.CharField(max_length=50)
    classification = models.CharField(max_length=20)
    details = models.ForeignKey(FrontendOrgdetails, models.DO_NOTHING)
    sub_category = models.ForeignKey(FrontendSubcategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'frontend_swda'


class FrontendSwdaWorkers(models.Model):
    id = models.BigAutoField(primary_key=True)
    swda = models.ForeignKey(FrontendSwda, models.DO_NOTHING)
    worker = models.ForeignKey('FrontendWorker', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'frontend_swda_workers'
        unique_together = (('swda', 'worker'),)


class FrontendTransactions(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateField()
    tstatus = models.IntegerField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING)
    level = models.ForeignKey(FrontendLevel, models.DO_NOTHING, blank=True, null=True)
    license = models.ForeignKey(FrontendLicense, models.DO_NOTHING)
    status = models.ForeignKey(FrontendStatus, models.DO_NOTHING, blank=True, null=True)
    transaction_type = models.ForeignKey('FrontendTransactiontype', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'frontend_transactions'


class FrontendTransactiontype(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=15)
    date_created = models.DateField()
    date_updated = models.DateField(blank=True, null=True)
    status = models.IntegerField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING)
    updated_by = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'frontend_transactiontype'


class FrontendWorker(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    extension = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=20)
    designation = models.ForeignKey(FrontendDesignation, models.DO_NOTHING)
    details = models.ForeignKey('FrontendWorkerdetails', models.DO_NOTHING, blank=True, null=True)
    pds_barangay_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'frontend_worker'


class FrontendWorkerdetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=40)
    landline = models.CharField(max_length=15)
    cellphone = models.CharField(max_length=15)
    fax = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'frontend_workerdetails'


class PdsBarangay(models.Model):
    name = models.CharField(max_length=128, db_collation='latin1_swedish_ci')
    city_code_id = models.IntegerField()
    status = models.IntegerField()
    upload_by_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pds_barangay'
        unique_together = (('id', 'city_code_id'),)


class PdsCity(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=24, db_collation='utf8_general_ci')
    prov_code_id = models.IntegerField()
    status = models.IntegerField()
    upload_by_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pds_city'
        unique_together = (('id', 'code'),)


class PdsProvince(models.Model):
    name = models.CharField(max_length=64, db_collation='latin1_swedish_ci')
    status = models.IntegerField()
    upload_by_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pds_province'
