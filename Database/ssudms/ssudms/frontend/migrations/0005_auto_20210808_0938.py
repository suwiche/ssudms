# Generated by Django 3.2.6 on 2021-08-08 01:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0004_auto_20210807_1318'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
    ]
