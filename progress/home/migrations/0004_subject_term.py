# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20150723_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='term',
            field=models.IntegerField(default=1, choices=[(1, 'Первый'), (2, 'Второй')]),
        ),
    ]
