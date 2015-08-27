# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20150823_1047'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='course',
            new_name='year',
        ),
    ]
