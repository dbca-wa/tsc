# Generated by Django 2.1.7 on 2019-05-14 08:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('occurrence', '0036_auto_20190514_1543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='areaassessment',
            name='survey_type',
        ),
        migrations.AlterField(
            model_name='areaencounter',
            name='source_id',
            field=models.CharField(default=uuid.UUID('f9949258-7620-11e9-a870-ecf4bb19b5fc'), help_text='The ID of the record in the original source, if available.', max_length=1000, verbose_name='Source ID'),
        ),
        migrations.DeleteModel(
            name='SurveyType',
        ),
    ]
