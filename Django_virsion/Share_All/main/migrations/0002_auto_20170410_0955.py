# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-10 09:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data',
            old_name='files',
            new_name='file_name',
        ),
        migrations.RenameField(
            model_name='data',
            old_name='urls',
            new_name='url',
        ),
    ]