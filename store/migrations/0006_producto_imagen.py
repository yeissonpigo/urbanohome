# Generated by Django 3.2.9 on 2021-11-29 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20211126_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='imagen',
            field=models.FileField(default=1, upload_to='media/'),
            preserve_default=False,
        ),
    ]