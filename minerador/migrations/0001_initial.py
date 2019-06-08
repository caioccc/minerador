# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-06-08 10:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('price', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('price', models.CharField(blank=True, max_length=100, null=True)),
                ('installments', models.CharField(blank=True, max_length=100, null=True)),
                ('sku', models.CharField(blank=True, max_length=100, null=True)),
                ('url', models.CharField(blank=True, max_length=300, null=True)),
                ('foto_url', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('url', models.CharField(blank=True, max_length=100, null=True)),
                ('done', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='minerador.Site'),
        ),
        migrations.AddField(
            model_name='history',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='minerador.Product'),
        ),
    ]
