# Generated by Django 3.0.2 on 2020-02-10 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0008_auto_20200209_1040'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='color',
            table='Color',
        ),
        migrations.AlterModelTable(
            name='size',
            table='Size',
        ),
        migrations.AlterModelTable(
            name='statusorder',
            table='StatusOrder',
        ),
    ]