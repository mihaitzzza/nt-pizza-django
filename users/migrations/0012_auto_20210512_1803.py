# Generated by Django 3.1.7 on 2021-05-12 18:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20210512_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activation',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 18, 33, 6, 432114, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='activation',
            name='token',
            field=models.CharField(default='285c4add51a34ad0b8062fae15f27d7a5415cc5f349de61a1f6616c3e6a509fc', max_length=64),
        ),
    ]
