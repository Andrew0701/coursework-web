# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_remove_subject_term'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='group',
            field=models.ForeignKey(to='home.Group', null=True),
        ),
    ]
