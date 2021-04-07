# Generated by Django 3.1.7 on 2021-03-31 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wiki', '0003_mptt_upgrade'),
        ('core', '0017_question_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionversion',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('PENDING', 'Pending')], default='PENDING', max_length=10)),
                ('message', models.TextField(blank=True, null=True)),
                ('article_revision', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wiki.articlerevision')),
                ('question_version', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.questionversion')),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_by', to=settings.AUTH_USER_MODEL)),
                ('submitted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submitted_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]