# Generated by Django 2.2.4 on 2019-10-26 17:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0003_remove_device_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupation_past_data',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
