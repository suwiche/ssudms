from django.db import models
from django.contrib.auth.models import User


class LibraryExtensions(models.Model):
    name = models.CharField(max_length=10)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='extensions_updated_by', on_delete=models.RESTRICT)
    status = models.IntegerField(default=1)


class LibraryTypes(models.Model):
    name = models.CharField(max_length=50)
    acronym = models.CharField(max_length=10)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='types_updated_by', on_delete=models.RESTRICT)
    status = models.IntegerField(default=1)
    has_worker = models.IntegerField(default=1)
    is_worker = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class LibraryProcess(models.Model):
    name = models.CharField(max_length=20)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='process_updated_by', on_delete=models.RESTRICT)
    status = models.IntegerField(default=1)


class LibraryProcessTypes(models.Model):
    name = models.CharField(max_length=20)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='process_types_updated_by', on_delete=models.RESTRICT)
    status = models.IntegerField(default=1)


class LibraryAgencyTypes(models.Model):
    name = models.CharField(max_length=20)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='agency_types_updated_by', on_delete=models.RESTRICT)
    status = models.IntegerField(default=1)


class LibraryServiceDeliveryModes(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='services_delivery_modes_updated_by', on_delete=models.RESTRICT)
    status = models.IntegerField(default=1)


class LibraryServices(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='services_updated_by', on_delete=models.RESTRICT)
    status = models.IntegerField(default=1)


class LibraryStatus(models.Model):
    name = models.CharField(max_length=20)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='status_updated_by', on_delete=models.RESTRICT)
    status = models.IntegerField(default=1)


class LibraryLevel(models.Model):
    name = models.CharField(max_length=10)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='level_updated_by', on_delete=models.RESTRICT)
    status = models.IntegerField(default=1)


class DetailsAttribute(models.Model):
    name = models.CharField(max_length=255)
    input_type = models.CharField(max_length=255)
    width = models.IntegerField()
    order = models.IntegerField()
    type = models.ForeignKey(LibraryTypes, related_name='type_id', on_delete=models.RESTRICT)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='details_attribute_updated_by',
                                   on_delete=models.RESTRICT)
    status = models.IntegerField(default=1)
    is_required = models.IntegerField(default=1)


class WorkerAttribute(models.Model):
    name = models.CharField(max_length=255)
    input_type = models.CharField(max_length=255)
    width = models.IntegerField()
    order = models.IntegerField()
    type = models.ForeignKey(LibraryTypes, related_name='worker_org_type_id', on_delete=models.RESTRICT)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='worker_attributes_updated_by',
                                   on_delete=models.RESTRICT)
    status = models.IntegerField(default=1)
    is_required = models.IntegerField(default=1)


class LibraryBarangay(models.Model):
    name = models.CharField(max_length=128)
    city_code = models.ForeignKey('LibraryCitymun', to_field='code', on_delete=models.DO_NOTHING)
    status = models.IntegerField()
    upload_by_id = models.IntegerField()


class LibraryCitymun(models.Model):
    name = models.CharField(max_length=64)
    code = models.IntegerField(unique=True)
    prov_code = models.ForeignKey('LibraryProvince', models.DO_NOTHING)
    status = models.IntegerField()
    upload_by_id = models.IntegerField()


class LibraryProvince(models.Model):
    name = models.CharField(max_length=64)
    status = models.IntegerField()
    upload_by_id = models.IntegerField()

    @property
    def get_count_of_cities(self):
        return LibraryCitymun.objects.filter(prov_code_id=self.id).count()


class Forms(models.Model):
    FORM_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('multiple', 'Multiple'),
        ('special', 'Special')
    ]
    name = models.CharField(max_length=50)
    org_type = models.ForeignKey(LibraryTypes, on_delete=models.DO_NOTHING)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='forms_updated_by', on_delete=models.RESTRICT)
    status = models.IntegerField(default=1)
    orientation = models.CharField(max_length=20)
    form_type = models.CharField(choices=FORM_TYPE_CHOICES, max_length=20)

    def __str__(self):
        return '{}'.format(self.name)


class FormVersions(models.Model):
    form = models.ForeignKey(Forms, on_delete=models.RESTRICT)
    name = models.CharField(max_length=50)
    template = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='forms_versions_updated_by', on_delete=models.RESTRICT)
    status = models.IntegerField(null=True)

    def __str__(self):
        return '{}'.format(self.name)
