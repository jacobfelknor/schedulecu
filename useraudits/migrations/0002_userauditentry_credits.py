# Generated by Django 2.2.8 on 2020-01-11 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraudits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userauditentry',
            name='credits',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
