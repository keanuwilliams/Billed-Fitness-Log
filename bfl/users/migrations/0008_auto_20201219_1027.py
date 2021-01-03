# Generated by Django 3.1.1 on 2020-12-19 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_profile_hide_resistance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='distance_units',
            field=models.CharField(choices=[('mi', 'mi'), ('km', 'km')], default='mi', max_length=3),
        ),
        migrations.AlterField(
            model_name='profile',
            name='weight_units',
            field=models.CharField(choices=[('lbs', 'lbs'), ('kg', 'kg'), ('st', 'st')], default='lbs', max_length=3),
        ),
    ]