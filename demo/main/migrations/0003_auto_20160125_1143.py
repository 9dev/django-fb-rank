# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20160125_1114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='path',
        ),
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
