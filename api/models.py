# from django.db import models

from djongo import models

class Product(models.Model):
    _id = models.ObjectIdField()
    productName = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    store = models.ObjectIdField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'products'

class Order(models.Model):
    _id = models.ObjectIdField()
    user = models.ObjectIdField()
    items = models.JSONField()
    totalCost = models.DecimalField(max_digits=10, decimal_places=2)
    shippingAddress = models.TextField()
    status = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'