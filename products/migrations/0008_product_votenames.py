# Generated by Django 2.0.5 on 2018-06-16 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_remove_product_votelist'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='votenames',
            field=models.TextField(default=False),
        ),
    ]