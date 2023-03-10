# Generated by Django 4.1.7 on 2023-03-12 00:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0004_project_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='avancement',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='avancement_reel',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='date_de_creation',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 12, 1, 33, 59, 672089)),
        ),
        migrations.AddField(
            model_name='task',
            name='date_debut_prevue',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='date_debut_reelle',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='date_fin_prevue',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='date_fin_reelle',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='date_modification',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='task',
            name='date_suppression',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='temps_estime',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='temps_estime_prevu',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='temps_estime_reel',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='temps_passe',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='temps_passe_prevu',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='temps_passe_reel',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='temps_reel',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='temps_restant',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='temps_restant_prevu',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='temps_restant_reel',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='type',
            field=models.CharField(default='T??che', max_length=200),
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('incomplete', 'Incompl??te'), ('complete', 'Compl??te')], max_length=20),
        ),
    ]
