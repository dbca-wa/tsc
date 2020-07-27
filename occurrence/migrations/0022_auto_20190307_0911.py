# Generated by Django 2.1.7 on 2019-03-07 01:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('occurrence', '0021_auto_20190306_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaAssessmentObservation',
            fields=[
                ('observationgroup_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='occurrence.ObservationGroup')),
                ('survey_type', models.CharField(choices=[('partial', 'Partial survey'), ('edge', 'Edge Survey'), ('full', 'Full Survey')], default='partial', help_text='How much of the occurrence has been surveyed?', max_length=100, verbose_name='Survey Type')),
                ('area_surveyed_m2', models.PositiveIntegerField(blank=True, help_text='An estimate of surveyed area in square meters.', null=True, verbose_name='Surveyed Area [m2]')),
                ('survey_duration_min', models.PositiveIntegerField(blank=True, help_text='An estimate of survey duration minutes.', null=True, verbose_name='Survey Duration [min]')),
            ],
            options={
                'verbose_name': 'Area Assessment',
                'verbose_name_plural': 'Area Assessments',
            },
            bases=('occurrence.observationgroup',),
        ),
        migrations.AlterModelOptions(
            name='fileattachmentobservation',
            options={'verbose_name': 'File Attachment', 'verbose_name_plural': 'File Attachments'},
        ),
        migrations.AlterField(
            model_name='areaencounter',
            name='source_id',
            field=models.CharField(default=uuid.UUID('ebe5126c-4075-11e9-a86f-40f02f6195e0'), help_text='The ID of the record in the original source, if available.', max_length=1000, verbose_name='Source ID'),
        ),
        migrations.AlterField(
            model_name='fileattachmentobservation',
            name='confidential',
            field=models.BooleanField(db_index=True, default=False, help_text='Whether this file is confidential or can be released to the public.', verbose_name='Is confidential'),
        ),
    ]
