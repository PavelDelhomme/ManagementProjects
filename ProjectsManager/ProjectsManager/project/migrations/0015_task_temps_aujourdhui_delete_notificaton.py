# Generated by Django 4.1.7 on 2023-03-13 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0014_notificaton'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='temps_aujourdhui',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Notificaton',
        ),
    ]
