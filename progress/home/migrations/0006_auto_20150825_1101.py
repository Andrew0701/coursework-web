# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20150823_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='semester',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='semester',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
