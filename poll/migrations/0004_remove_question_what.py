# Generated by Django 4.1.3 on 2022-11-22 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0003_alter_question_what'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='what',
        ),
    ]
