# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-06-08 11:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minerador', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='history',
            old_name='published_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='published_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='site',
            old_name='published_at',
            new_name='updated_at',
        ),
    ]
