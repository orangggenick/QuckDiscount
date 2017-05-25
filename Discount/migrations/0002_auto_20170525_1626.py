# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-25 16:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Discount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('stock_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Favorites',
            },
        ),
        migrations.AlterField(
            model_name='stock',
            name='terms',
            field=models.DateField(),
        ),
    ]
