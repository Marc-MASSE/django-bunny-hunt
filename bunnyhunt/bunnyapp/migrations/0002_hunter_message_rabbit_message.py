# Generated by Django 4.2.6 on 2023-10-12 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bunnyapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hunter',
            name='message',
            field=models.CharField(default='None', max_length=24),
        ),
        migrations.AddField(
            model_name='rabbit',
            name='message',
            field=models.CharField(default='None', max_length=24),
        ),
    ]