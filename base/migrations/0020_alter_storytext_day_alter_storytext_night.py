# Generated by Django 5.0 on 2024-12-08 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_storytext_day_storytext_night_alter_game_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storytext',
            name='day',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Наступление дня'),
        ),
        migrations.AlterField(
            model_name='storytext',
            name='night',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Наступление ночи'),
        ),
    ]