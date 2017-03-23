# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 20:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProviderRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='name')),
                ('regex', models.CharField(max_length=2000, verbose_name='regex')),
                ('endpoint', models.CharField(max_length=2000, verbose_name='endpoint')),
                ('format', models.IntegerField(choices=[(1, 'JSON'), (2, 'XML')], verbose_name='format')),
                ('simple', models.BooleanField(default=False, help_text='Specify whether this provider generates a simple,                            minimalistic embed object.', verbose_name='simple')),
            ],
            options={
                'ordering': ('name', 'endpoint'),
            },
        ),
        migrations.CreateModel(
            name='StoredOEmbed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match', models.TextField(verbose_name='match')),
                ('max_width', models.IntegerField(verbose_name='max width')),
                ('max_height', models.IntegerField(verbose_name='max height')),
                ('html', models.TextField(verbose_name='html')),
                ('json', models.TextField(verbose_name='json')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date added')),
                ('simple', models.BooleanField(default=False, help_text='Specify whether this is a simple, minimalistic                            embed object.', verbose_name='simple')),
            ],
            options={
                'verbose_name': 'Stored oEmbed',
                'ordering': ('-max_width',),
                'verbose_name_plural': 'Stored oEmbeds',
            },
        ),
    ]
