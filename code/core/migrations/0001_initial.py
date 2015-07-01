# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('contact_name', models.CharField(max_length=100, null=True, blank=True)),
                ('contact_email', models.EmailField(max_length=200)),
                ('contact_comment', models.TextField()),
            ],
        ),
    ]
