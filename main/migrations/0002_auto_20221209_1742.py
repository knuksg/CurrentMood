# Generated by Django 3.2.13 on 2022-12-09 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='channel',
            field=models.CharField(default=None, max_length=130, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='default',
            field=models.CharField(default=None, max_length=130, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='hqdefault',
            field=models.CharField(default=None, max_length=130, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='mqdefault',
            field=models.CharField(default=None, max_length=130, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='title',
            field=models.CharField(default=None, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='vidid',
            field=models.CharField(default=None, max_length=130, null=True),
        ),
    ]
