# Generated by Django 2.2.6 on 2019-11-18 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='audit',
            name='currentMajorCredit',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='audit',
            name='majorRequirement',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]