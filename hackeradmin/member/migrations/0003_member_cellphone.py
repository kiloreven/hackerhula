# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_physicalaccess'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='cellphone',
            field=models.CharField(max_length=200, verbose_name=b'Cellhone number)', blank=True),
        ),
    ]
