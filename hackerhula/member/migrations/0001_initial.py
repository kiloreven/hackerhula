# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('memberid', models.IntegerField(help_text=b'Four digits, increasing from 1000.', unique=True)),
                ('name', models.CharField(max_length=200)),
                ('handle', models.CharField(max_length=200, blank=True)),
                ('address', models.CharField(max_length=500)),
                ('picture', models.ImageField(upload_to=b'', verbose_name=b'Picture of member (keycard?).', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name=b'Member email address')),
                ('member_since', models.DateTimeField(auto_now_add=True, verbose_name=b'Initially registered')),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('access_card', models.CharField(max_length=200, blank=True)),
                ('unix_username', models.CharField(max_length=200, blank=True)),
                ('unix_uid', models.IntegerField(null=True, blank=True)),
                ('authorized_keys', models.TextField(verbose_name=b'SSH public keys', blank=True)),
                ('hausmania_keynumber', models.IntegerField(null=True, verbose_name=b'Hausmania key serial number', blank=True)),
                ('hausmania_deposit', models.BooleanField(default=False, verbose_name=b'Has key deposit been paid by member?')),
                ('nettlaug_member', models.BooleanField(default=False)),
                ('active_membership', models.BooleanField(default=True, help_text=b'The big knob. Disable if member is not active any more.', verbose_name=b'Has the member an active membership?')),
                ('comment', models.TextField(verbose_name=b'Additional notes for this member.', blank=True)),
            ],
        ),
    ]
