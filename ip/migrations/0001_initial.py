# Generated by Django 2.1.7 on 2019-02-24 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=15, unique=True)),
                ('country_name', models.CharField(max_length=100)),
                ('country_flag', models.CharField(blank=True, max_length=100)),
                ('region_name', models.CharField(max_length=100)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('latitude', models.DecimalField(decimal_places=4, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=4, max_digits=7)),
            ],
        ),
    ]
