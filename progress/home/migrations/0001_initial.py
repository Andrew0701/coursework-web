# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.CharField(max_length=5)),
                ('course', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('number', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mark', models.IntegerField()),
                ('date', models.DateField()),
                ('job', models.ForeignKey(to='home.Job')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('patronymic', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('group', models.ForeignKey(null=True, to='home.Group')),
                ('jobs', models.ManyToManyField(to='home.Job', through='home.Log')),
            ],
        ),
        migrations.CreateModel(
            name='Student_Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('student', models.ForeignKey(to='home.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('patronymic', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('subjects', models.ManyToManyField(to='home.Subject')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='student_subject',
            name='subject',
            field=models.ForeignKey(to='home.Subject'),
        ),
        migrations.AddField(
            model_name='student_subject',
            name='teacher',
            field=models.ForeignKey(to='home.Teacher'),
        ),
        migrations.AddField(
            model_name='student',
            name='subjects',
            field=models.ManyToManyField(to='home.Subject', through='home.Student_Subject'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='log',
            name='student',
            field=models.ForeignKey(to='home.Student'),
        ),
        migrations.AddField(
            model_name='job',
            name='subject',
            field=models.ForeignKey(to='home.Subject'),
        ),
    ]
