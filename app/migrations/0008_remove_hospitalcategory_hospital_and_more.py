# Generated by Django 4.2 on 2024-06-13 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_availabledays_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospitalcategory',
            name='hospital',
        ),
        migrations.AddField(
            model_name='hospitalcategory',
            name='hospital',
            field=models.ManyToManyField(related_name='hospital_category', to='app.hospital'),
        ),
    ]
