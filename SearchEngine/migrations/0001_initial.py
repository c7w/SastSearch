# Generated by Django 3.2.5 on 2021-08-01 09:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RegVerify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=20)),
                ('createdAt', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
    ]
