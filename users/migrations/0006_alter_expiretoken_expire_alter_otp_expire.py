# Generated by Django 5.2.1 on 2025-05-23 08:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_expiretoken_expire_alter_otp_expire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expiretoken',
            name='expire',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 23, 8, 51, 3, 154682, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='otp',
            name='expire',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 23, 8, 51, 3, 154970, tzinfo=datetime.timezone.utc)),
        ),
    ]
