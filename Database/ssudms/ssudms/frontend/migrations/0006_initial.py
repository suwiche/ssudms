# Generated by Django 3.2.6 on 2021-08-08 02:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('frontend', '0005_auto_20210808_0938'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField()),
                ('status', models.IntegerField(default=1)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='updated_by_category', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(null=True)),
                ('status', models.IntegerField(default=1)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='updated_by_designation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(null=True)),
                ('status', models.IntegerField(default=1)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='level_updated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_issued', models.DateField(null=True)),
                ('date_expired', models.DateField(null=True)),
                ('license_key', models.CharField(max_length=50)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='OrgDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=40)),
                ('landline', models.CharField(max_length=15)),
                ('cellphone', models.CharField(max_length=15)),
                ('fax', models.CharField(max_length=15)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='frontend.org')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(null=True)),
                ('status', models.IntegerField(default=1)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='status_updated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField()),
                ('status', models.IntegerField(default=1)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='frontend.category')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='updated_by_subcategory', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30)),
                ('extension', models.CharField(blank=True, choices=[('', 'None'), ('Jr.', 'Jr.'), ('Jr', 'Sr.'), ('I', 'I'), ('II', 'II'), ('III', 'III')], max_length=10, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Rather_not_to_say', 'Rather not to say')], max_length=20)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('designation', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='frontend.designation')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='updated_by_worker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(null=True)),
                ('status', models.IntegerField(default=1)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='transaction_type_updated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('tstatus', models.IntegerField(default=1)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='frontend.level')),
                ('license', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='frontend.license')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='frontend.status')),
                ('transaction_type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='frontend.transactiontype')),
            ],
        ),
        migrations.CreateModel(
            name='Swda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('services', models.CharField(max_length=255)),
                ('clientele', models.CharField(max_length=50)),
                ('service_delivery_mode', models.CharField(max_length=50)),
                ('area_operation', models.CharField(max_length=50)),
                ('remarks', models.CharField(max_length=50)),
                ('classification', models.CharField(max_length=20)),
                ('details', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='frontend.orgdetails')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='frontend.subcategory')),
                ('workers', models.ManyToManyField(to='frontend.Worker')),
            ],
        ),
        migrations.CreateModel(
            name='OrgType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(null=True)),
                ('status', models.IntegerField(default=1)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='org_type_updated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='orgdetails',
            name='transactions',
            field=models.ManyToManyField(to='frontend.Transactions'),
        ),
        migrations.AddField(
            model_name='org',
            name='org_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='frontend.orgtype'),
        ),
        migrations.CreateModel(
            name='Cso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ga', models.CharField(max_length=20)),
                ('approved_program', models.CharField(max_length=100)),
                ('details', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='frontend.orgdetails')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='frontend.worker')),
            ],
        ),
        migrations.CreateModel(
            name='Cdw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='frontend.orgdetails')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='frontend.worker')),
            ],
        ),
        migrations.CreateModel(
            name='Cdc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='frontend.orgdetails')),
                ('workers', models.ManyToManyField(to='frontend.Cdw')),
            ],
        ),
    ]
