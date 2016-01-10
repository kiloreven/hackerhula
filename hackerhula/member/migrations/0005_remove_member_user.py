# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_member_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='user',
        ),
    ]
