# Generated by Django 5.0 on 2024-10-13 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_role_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='effect',
        ),
        migrations.AddField(
            model_name='user',
            name='effect',
            field=models.ManyToManyField(blank=True, to='base.effect', verbose_name='Действующий эффект'),
        ),
    ]
