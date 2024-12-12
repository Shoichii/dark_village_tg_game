# Generated by Django 5.0 on 2024-12-12 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_ability_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameprocessjournal',
            name='selected_action',
            field=models.CharField(blank=True, choices=[('infect', 'Заразить'), ('kill', 'Убить')], max_length=255, null=True, verbose_name='Выбранное действие'),
        ),
        migrations.AlterField(
            model_name='gameprocessjournal',
            name='current_buffs',
            field=models.ManyToManyField(blank=True, to='base.buff', verbose_name='Баффы'),
        ),
        migrations.AlterField(
            model_name='gameprocessjournal',
            name='current_debuffs',
            field=models.ManyToManyField(blank=True, to='base.debuff', verbose_name='Дебаффы'),
        ),
    ]
