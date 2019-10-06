import uuid

from django.db import models


class WishList(models.Model):
    customer = models.ForeignKey(
        'customer.Customer',
        related_name='wishlist',
        on_delete=models.CASCADE
    )
    product_id = models.UUIDField(default=uuid.uuid4, db_index=True)

    class Meta:
        db_table = 'wish_list'
