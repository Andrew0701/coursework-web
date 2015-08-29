# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20150825_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='log',
            name='mark',
            field=models.IntegerField(null=True),
        ),
    ]
