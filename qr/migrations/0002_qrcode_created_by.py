# Generated by Django 5.2.4 on 2025-07-03 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='qrcode',
            name='created_by',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
