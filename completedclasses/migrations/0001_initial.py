# Generated by Django 2.2.6 on 2019-11-21 03:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_user_major'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompletedClasses',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='completed', serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
