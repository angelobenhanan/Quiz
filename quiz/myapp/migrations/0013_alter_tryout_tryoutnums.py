# Generated by Django 5.1.6 on 2025-03-08 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_question_answer_delete_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tryout',
            name='tryoutNums',
            field=models.IntegerField(default=0),
        ),
    ]
