# Generated by Django 2.2.6 on 2019-11-27 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fcq', '0002_remove_fcq_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
        migrations.RemoveField(
            model_name='fcq',
            name='courseTitle',
        ),
        migrations.RemoveField(
            model_name='fcq',
            name='department',
        ),
        migrations.RemoveField(
            model_name='fcq',
            name='index',
        ),
        migrations.RemoveField(
            model_name='fcq',
            name='level',
        ),
        migrations.RemoveField(
            model_name='fcq',
            name='section',
        ),
        migrations.AddField(
            model_name='fcq',
            name='challenge',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='fcq',
            name='courseRating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='fcq',
            name='courseSD',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='fcq',
            name='learned',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='fcq',
            name='numResponses',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='fcq',
            name='profEffect',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='fcq',
            name='profRating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='fcq',
            name='profSD',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='fcq',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fcqs', to='classes.Class'),
        ),
        migrations.AlterField(
            model_name='fcq',
            name='courseType',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='fcq',
            name='online',
            field=models.CharField(max_length=1),
        ),
        migrations.AlterField(
            model_name='fcq',
            name='semester',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='fcq',
            name='size',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='fcq',
            name='year',
            field=models.CharField(max_length=4),
        ),
        migrations.AddField(
            model_name='fcq',
            name='professor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fcqs', to='fcq.Professor'),
        ),
    ]
