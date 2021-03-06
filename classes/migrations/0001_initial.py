# Generated by Django 2.2.6 on 2019-10-26 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=4)),
                ('course_subject', models.IntegerField()),
                ('section_number', models.CharField(max_length=5)),
                ('session', models.CharField(max_length=3)),
                ('class_number', models.IntegerField()),
                ('credit', models.CharField(max_length=3)),
                ('course_title', models.CharField(max_length=50)),
                ('start_time', models.CharField(blank=True, max_length=10, null=True)),
                ('end_time', models.CharField(blank=True, max_length=10, null=True)),
                ('days', models.CharField(blank=True, max_length=10, null=True)),
                ('building_room', models.CharField(blank=True, max_length=40, null=True)),
                ('instructor_name', models.CharField(blank=True, max_length=50, null=True)),
                ('max_enrollment', models.IntegerField()),
                ('campus', models.CharField(max_length=15)),
            ],
        ),
    ]
