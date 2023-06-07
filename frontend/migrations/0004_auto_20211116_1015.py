# Generated by Django 3.2.7 on 2021-11-16 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20211116_1012'),
        ('frontend', '0003_transaction_remarks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='org',
            name='service',
        ),
        migrations.CreateModel(
            name='OrgService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='frontend.org')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='backend.libraryservices')),
                ('service_delivery_mode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='backend.libraryservicedeliverymodes')),
            ],
        ),
    ]
