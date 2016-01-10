# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0005_remove_member_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name=b'When the membership entry was first added')),
                ('changed_at', models.DateTimeField(auto_now=True, verbose_name=b'When was the membership entry last changed.')),
                ('paid', models.BooleanField(default=True, verbose_name=b'Has this membership been paid?')),
                ('start_date', models.DateField(auto_now_add=True, verbose_name=b'Membership start date')),
                ('running', models.BooleanField(default=False, verbose_name=b'This membership is continuous')),
                ('end_date', models.DateField(null=True, verbose_name=b'Membership end date. NOOP if is continuous.')),
                ('description', models.TextField(verbose_name=b'Additional notes', blank=True)),
                ('member', models.ForeignKey(to='member.Member')),
            ],
        ),
    ]
