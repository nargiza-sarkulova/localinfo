# Generated by Django 2.1.7 on 2019-02-24 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ip', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ip',
            name='country_code',
            field=models.CharField(default='ca', max_length=2),
            preserve_default=False,
        ),
    ]
