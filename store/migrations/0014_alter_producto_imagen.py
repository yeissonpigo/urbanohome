# Generated by Django 4.0.5 on 2022-06-15 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_venta_referencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.FileField(upload_to='media'),
        ),
    ]