# Generated by Django 3.1.8 on 2021-04-19 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0028_auto_20210419_1541'),
    ]

    operations = [
        migrations.RenameField(
            model_name='events',
            old_name='newsletter',
            new_name='newsletter_link',
        ),
        migrations.RenameField(
            model_name='events',
            old_name='youtube',
            new_name='youtube_link',
        ),
    ]