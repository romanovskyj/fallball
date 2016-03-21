# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filesharing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='admin',
            field=models.CharField(default='test@company.name', max_length=120),
            preserve_default=False,
        ),
    ]
