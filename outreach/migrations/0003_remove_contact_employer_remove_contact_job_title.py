# Generated by Django 5.0 on 2024-09-29 01:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outreach', '0002_alter_studentenrollment_enrollment_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='employer',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='job_title',
        ),
    ]
