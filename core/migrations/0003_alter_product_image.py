# Generated by Django 4.2.10 on 2024-02-18 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.URLField(blank=True, null=True, verbose_name='Фото'),
        ),
    ]
