# Generated by Django 5.0 on 2024-12-08 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_storytext'),
    ]

    operations = [
        migrations.AddField(
            model_name='storytext',
            name='day',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='storytext',
            name='night',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('waiting', 'Ожидание игроков'), ('finished', 'Игра закончилась'), ('canceled', 'Игра отменена'), ('Day', 'День'), ('Night', 'Ночь')], default='waiting', max_length=255, verbose_name='Статус'),
        ),
    ]
