# Generated by Django 2.1.1 on 2018-10-17 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20181017_0321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='address',
        ),
        migrations.RemoveField(
            model_name='book',
            name='bathrooms',
        ),
        migrations.RemoveField(
            model_name='book',
            name='bedrooms',
        ),
        migrations.RemoveField(
            model_name='book',
            name='city',
        ),
        migrations.RemoveField(
            model_name='book',
            name='garage',
        ),
        migrations.RemoveField(
            model_name='book',
            name='lot_size',
        ),
        migrations.RemoveField(
            model_name='book',
            name='sqft',
        ),
        migrations.RemoveField(
            model_name='book',
            name='state',
        ),
        migrations.RemoveField(
            model_name='book',
            name='zipcode',
        ),
    ]
