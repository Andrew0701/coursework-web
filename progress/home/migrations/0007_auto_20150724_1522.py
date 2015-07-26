# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0006_student_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
