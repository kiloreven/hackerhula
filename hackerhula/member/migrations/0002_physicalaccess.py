# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhysicalAccess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cardname', models.CharField(max_length=200, verbose_name=b'Short name/description of the card')),
                ('contactinfo', models.CharField(max_length=200, verbose_name=b'Name and cellphone to person in charge of card')),
                ('enabled', models.BooleanField(default=True, help_text=b'Only applies if within the described time frame.', verbose_name=b'Is this access card enabled?')),
                ('access_token', models.CharField(unique=True, max_length=200, verbose_name=b'Access token presented by card.')),
                ('access_start', models.DateTimeField(default=datetime.datetime.utcnow, verbose_name=b'Card is valid starting from')),
                ('access_end', models.DateTimeField(verbose_name=b'Card is valid until')),
                ('description', models.TextField(verbose_name=b'Additional notes', blank=True)),
            ],
        ),
    ]
