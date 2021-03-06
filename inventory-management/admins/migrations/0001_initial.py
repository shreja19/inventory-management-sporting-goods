# Generated by Django 2.2 on 2021-11-22 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_description', models.CharField(max_length=1000)),
                ('price_per_unit', models.FloatField()),
                ('discount_per_unit', models.FloatField()),
                ('category_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'products',
            },
        ),
    ]
