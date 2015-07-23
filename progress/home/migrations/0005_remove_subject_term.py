# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_subject_term'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='term',
        ),
    ]
