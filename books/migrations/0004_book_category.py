# Generated by Django 2.1.1 on 2018-10-18 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20181017_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.CharField(default='Otros', max_length=200),
            preserve_default=False,
        ),
    ]