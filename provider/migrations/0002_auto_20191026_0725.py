# Generated by Django 2.2.4 on 2019-10-26 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opening_dates',
            name='closing_noon',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='opening_dates',
            name='opening_noon',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
