# Generated by Django 2.0.8 on 2018-09-26 03:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conservation', '0001_squashed_0027_auto_20180509_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileattachment',
            name='author',
            field=models.ForeignKey(blank=True, help_text='The person who authored and endorsed this file.', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
    ]
