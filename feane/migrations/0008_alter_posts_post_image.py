# Generated by Django 4.2.3 on 2023-08-04 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feane', '0007_alter_product_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='post_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]