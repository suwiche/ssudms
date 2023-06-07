from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class LandingPage(models.Model):
    title = models.CharField(max_length=155)
    description = models.CharField(max_length=155)
    type = models.CharField(maxlength=155)
    image = models.ImageField(null=True, blank=True)
    icon_code = models.CharField(max_length=80, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_updated = models.DateField(auto_now_add=False, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='types_updated_by', on_delete=models.RESTRICT)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'landingpage'