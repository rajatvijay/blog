# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20160425_1303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='updates',
            new_name='updated',
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 25, 13, 10, 43, 679758, tzinfo=utc)),
        ),
    ]
