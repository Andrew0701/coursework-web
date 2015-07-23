# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_course'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Course',
            new_name='Group',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='number',
            new_name='course',
        ),
    ]
