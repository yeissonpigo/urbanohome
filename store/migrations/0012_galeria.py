# Generated by Django 3.2.9 on 2022-03-22 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_venta_direccion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Galeria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.FileField(upload_to='media/')),
            ],
        ),
    ]