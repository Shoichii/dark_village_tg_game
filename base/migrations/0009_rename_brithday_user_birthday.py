# Generated by Django 5.0 on 2024-10-15 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_user_brithday'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='brithday',
            new_name='birthday',
        ),
    ]