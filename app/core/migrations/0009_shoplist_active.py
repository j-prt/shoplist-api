# Generated by Django 4.0.8 on 2022-11-08 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoplist',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ]
