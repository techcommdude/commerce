# Generated by Django 4.1.3 on 2022-12-13 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_listings_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='category',
            field=models.CharField(choices=[('Cars', 'Car'), ('Appliances', 'Appliances'), ('Sports', 'Sports'), ('NewCategory', 'NewCategory')], default='Cars', max_length=64),
        ),
    ]
