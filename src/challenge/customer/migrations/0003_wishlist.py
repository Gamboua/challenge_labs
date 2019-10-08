# Generated by Django 2.2 on 2019-10-07 21:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20191005_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.UUIDField(db_index=True, default=uuid.uuid4)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to='customer.Customer')),
            ],
            options={
                'db_table': 'wish_list',
            },
        ),
    ]