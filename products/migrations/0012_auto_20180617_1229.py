# Generated by Django 2.0.6 on 2018-06-17 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20180617_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, default=True, max_length=25, null=True),
        ),
    ]
