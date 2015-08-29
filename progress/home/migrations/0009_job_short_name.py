# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_subject_short_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='short_name',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
