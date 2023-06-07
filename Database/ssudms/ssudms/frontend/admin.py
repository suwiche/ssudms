from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(OrgType)
admin.site.register(Org)
admin.site.register(OrgDetails)
admin.site.register(Designation)
admin.site.register(Worker)
admin.site.register(WorkerDetails)
admin.site.register(Docs)
admin.site.register(Status)
admin.site.register(Level)
admin.site.register(Transactions)
admin.site.register(TransactionType)
admin.site.register(License)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Cso)
admin.site.register(Cdc)
admin.site.register(Cdw)
admin.site.register(Swda)
admin.site.register(PdsBarangay)
admin.site.register(PdsCity)
admin.site.register(PdsProvince)
