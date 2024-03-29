# Generated by Django 3.1.2 on 2020-10-06 13:19

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0019_auto_20201002_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True)),
                ('paragraphs', wagtail.core.fields.RichTextField(blank=True)),
                ('problems', wagtail.core.fields.RichTextField(blank=True)),
                ('sachverhalt_link', models.CharField(max_length=255)),
                ('loesung_link', models.CharField(max_length=255)),
                ('difficulty', models.CharField(blank=True, choices=[('beginner', 'Anfänger'), ('intermediate', 'Fortgeschrittene'), ('advanced', 'Examen')], max_length=255)),
                ('type', models.CharField(blank=True, choices=[('falltraining', 'Klausur im Falltraining'), ('exam', 'Examensklausur'), ('original-exam', 'Originalexamensklausur'), ('exercise', 'Übungsfall'), ('tutorial', 'AG-Fall')], max_length=255)),
            ],
            options={
                'verbose_name': 'Exams',
            },
        ),
    ]
