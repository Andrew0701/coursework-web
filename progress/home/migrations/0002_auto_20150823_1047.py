# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='number',
        ),
        migrations.AlterField(
            model_name='group',
            name='group',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='job',
            name='name',
            field=models.CharField(max_length=512),
        ),
    ]
