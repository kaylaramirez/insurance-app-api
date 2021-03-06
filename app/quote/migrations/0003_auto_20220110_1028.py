# Generated by Django 2.2.26 on 2022-01-10 10:28

import django.core.validators
from django.db import migrations, models
import quote.models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0002_auto_20220110_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='street_address_2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='quote',
            name='quote_id',
            field=models.CharField(default=quote.models.Quote.generate_quote_id, max_length=10, validators=[django.core.validators.MinLengthValidator(10)]),
        ),
    ]
