# Generated by Django 3.2.7 on 2021-11-17 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0007_worker_barangay'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker',
            name='barangay',
        ),
    ]
