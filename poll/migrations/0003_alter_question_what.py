# Generated by Django 4.1.3 on 2022-11-22 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0002_question_what'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='what',
            field=models.BooleanField(default=False),
        ),
    ]
