# Generated by Django 2.1.1 on 2018-11-20 03:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Excel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_modified_past', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('title', models.TextField(blank=True)),
            ],
        ),
    ]
