# Generated by Django 3.2.13 on 2022-12-01 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20221201_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='place',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]
