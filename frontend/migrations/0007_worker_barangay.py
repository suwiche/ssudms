# Generated by Django 3.2.7 on 2021-11-17 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20211116_1012'),
        ('frontend', '0006_auto_20211116_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='barangay',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='backend.librarybarangay'),
        ),
    ]
