# Generated by Django 5.0 on 2024-12-11 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_delete_storytext'),
    ]

    operations = [
        migrations.AddField(
            model_name='buff',
            name='key',
            field=models.CharField(default=1, max_length=255, verbose_name='Ключ'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='debuff',
            name='key',
            field=models.CharField(default=1, max_length=255, verbose_name='Ключ'),
            preserve_default=False,
        ),
    ]
