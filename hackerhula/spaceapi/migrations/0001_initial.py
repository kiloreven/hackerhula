# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoomState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('roomname', models.CharField(max_length=255, verbose_name=b'Which room/area is concerned by this record?')),
                ('is_open', models.BooleanField(default=False, verbose_name=b'Is the room open right now?')),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
