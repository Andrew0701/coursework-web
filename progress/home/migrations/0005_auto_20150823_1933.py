# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_semester'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='group',
            new_name='name',
        ),
    ]
