# Generated by Django 2.0.6 on 2019-03-12 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20190312_0308'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersong',
            name='mimetype',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]