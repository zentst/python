# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20150508_1936'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todolist',
            old_name='list_text',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='todolist',
            old_name='list_name',
            new_name='subject',
        ),
    ]
