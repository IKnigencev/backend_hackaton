# Generated by Django 4.2 on 2023-04-19 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_controller_clients_controller_server_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='werehouse',
            name='address',
        ),
    ]
