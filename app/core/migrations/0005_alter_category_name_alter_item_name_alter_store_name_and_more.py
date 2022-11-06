# Generated by Django 4.0.8 on 2022-11-04 20:24

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_item_category_item_category_remove_item_store_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=core.models.NameField(max_length=64),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=core.models.NameField(max_length=64),
        ),
        migrations.AlterField(
            model_name='store',
            name='name',
            field=core.models.NameField(max_length=64),
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('name', 'user'), name='unique_category'),
        ),
        migrations.AddConstraint(
            model_name='item',
            constraint=models.UniqueConstraint(fields=('name', 'user'), name='unique_item'),
        ),
        migrations.AddConstraint(
            model_name='store',
            constraint=models.UniqueConstraint(fields=('name', 'user'), name='unique_store'),
        ),
    ]