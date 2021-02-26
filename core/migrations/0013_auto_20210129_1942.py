# Generated by Django 3.0.10 on 2021-01-29 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0003_mptt_upgrade'),
        ('core', '0012_merge_20210122_1617'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionversion',
            name='category',
        ),
        migrations.AddField(
            model_name='questionversion',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, to='wiki.Article'),
        ),
    ]