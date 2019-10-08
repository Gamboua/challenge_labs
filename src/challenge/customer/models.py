import uuid

from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=140)
    email = models.CharField(max_length=140, unique=True)

    class Meta:
        db_table = 'customer'


class WishList(models.Model):
    customer = models.ForeignKey(
        'Customer',
        related_name='wishlist',
        on_delete=models.CASCADE
    )
    product_id = models.UUIDField(default=uuid.uuid4, db_index=True)

    class Meta:
        db_table = 'wish_list'
