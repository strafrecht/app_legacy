# Generated by Django 3.1.7 on 2021-04-07 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_autor_libro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libro',
            name='autor',
        ),
        migrations.DeleteModel(
            name='Autor',
        ),
        migrations.DeleteModel(
            name='Libro',
        ),
    ]