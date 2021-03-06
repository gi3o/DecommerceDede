# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-22 07:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decommerce', '0004_auto_20170519_1557'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'order'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'product'},
        ),
        migrations.AlterModelOptions(
            name='productreview',
            options={'verbose_name': 'product review'},
        ),
        migrations.AlterModelOptions(
            name='sellerprofile',
            options={'verbose_name': 'seller profile'},
        ),
        migrations.AlterModelOptions(
            name='sellerreview',
            options={'verbose_name': 'seller review'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'user profile'},
        ),
        migrations.RenameField(
            model_name='productreview',
            old_name='starts',
            new_name='stars',
        ),
    ]
