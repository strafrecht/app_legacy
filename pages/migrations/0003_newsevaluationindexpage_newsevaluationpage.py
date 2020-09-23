# Generated by Django 3.0.10 on 2020-09-15 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0052_pagelogentry'),
        ('pages', '0002_newsnewsletterpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsEvaluationIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='NewsEvaluationPage',
            fields=[
                ('websitepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.WebsitePage')),
            ],
            options={
                'abstract': False,
            },
            bases=('pages.websitepage',),
        ),
    ]
