# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-08 23:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minerador', '0005_auto_20190608_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
