# Generated by Django 3.2.6 on 2021-08-07 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_rename_books_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
