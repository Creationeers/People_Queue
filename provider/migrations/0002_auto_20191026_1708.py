# Generated by Django 2.2.4 on 2019-10-26 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='provider.Profile'),
        ),
    ]
