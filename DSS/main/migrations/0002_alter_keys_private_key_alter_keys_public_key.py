# Generated by Django 4.0.2 on 2022-03-16 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keys',
            name='private_key',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='keys',
            name='public_key',
            field=models.BinaryField(),
        ),
    ]
