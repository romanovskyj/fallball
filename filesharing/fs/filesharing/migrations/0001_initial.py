# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('companyname', models.CharField(max_length=100)),
                ('diskusage', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Reseller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('partnerid', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='resellerid',
            field=models.ForeignKey(to='filesharing.Reseller'),
        ),
    ]
