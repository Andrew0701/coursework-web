# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20150827_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='short_name',
            field=models.CharField(unique=True, null=True, max_length=10),
        ),
    ]
