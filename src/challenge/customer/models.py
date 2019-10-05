from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=140)
    email = models.CharField(max_length=140)

    class Meta:
        db_table = 'customer'