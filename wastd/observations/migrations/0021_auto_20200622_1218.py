# Generated by Django 2.2.10 on 2020-06-22 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0020_auto_20200622_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='encounter',
            name='location_accuracy_m',
            field=models.FloatField(blank=True, help_text='The accuracy of the supplied location in metres, if given.', null=True, verbose_name='Location accuracy (m)'),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='location_accuracy',
            field=models.CharField(choices=[('10', 'GPS reading at exact location (10 m)'), ('1000', 'Site centroid or place name (1 km)'), ('10000', 'Rough estimate (10 km)')], default='1000', help_text='The source of the supplied location implies a rough location accuracy.', max_length=300, verbose_name='Location accuracy class (m)'),
        ),
        migrations.AlterField(
            model_name='turtlehatchlingemergenceobservation',
            name='light_sources_present',
            field=models.CharField(choices=[('na', 'NA'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Light sources present during emergence'),
        ),
        migrations.AlterField(
            model_name='turtlehatchlingemergenceobservation',
            name='outlier_tracks_present',
            field=models.CharField(choices=[('na', 'NA'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Outlier tracks present'),
        ),
        migrations.AlterField(
            model_name='turtlehatchlingemergenceoutlierobservation',
            name='outlier_group_size',
            field=models.PositiveIntegerField(blank=True, help_text='', null=True, verbose_name='Number of tracks in outlier group'),
        ),
    ]
