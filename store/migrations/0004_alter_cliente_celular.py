# Generated by Django 3.2.9 on 2021-11-26 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20211126_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='celular',
            field=models.BigIntegerField(),
        ),
    ]
