# Generated by Django 3.1.2 on 2020-10-06 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0020_exams'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exams',
            name='loesung_link',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='exams',
            name='sachverhalt_link',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
