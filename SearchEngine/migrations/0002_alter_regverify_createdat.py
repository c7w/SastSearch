# Generated by Django 3.2.5 on 2021-08-01 09:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('SearchEngine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regverify',
            name='createdAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]