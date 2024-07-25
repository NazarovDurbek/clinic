# Generated by Django 4.2 on 2024-06-11 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_alter_timeslot_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='patient',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_time_slot', to=settings.AUTH_USER_MODEL),
        ),
    ]
