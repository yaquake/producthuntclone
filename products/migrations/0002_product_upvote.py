# Generated by Django 2.0.5 on 2018-06-16 00:36

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='upvote',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=15), null=True, size=None),
        ),
    ]