# Generated by Django 4.2.3 on 2023-08-03 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('number', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('num_of_persons', models.PositiveIntegerField(choices=[(2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.CharField(default=0.0, max_length=200)),
                ('limit', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('subtitle', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('discounted_price', models.DecimalField(decimal_places=2, default='0.00', max_digits=5)),
                ('product_image', models.ImageField(upload_to='images/')),
                ('product_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='feane.product_category')),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('subtitle', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.TextField()),
                ('post_image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='feane.category')),
            ],
        ),
    ]
