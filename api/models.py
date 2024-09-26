# from django.db import models

from djongo import models

class User(models.Model):

    _id = models.ObjectIdField()
    email = models.CharField(max_length=255)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)

    class Meta:
        db_table = 'user'


class Store(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.EmbeddedField(model_container=User)

    class Meta:
        db_table = 'store'

class Products(models.Model):
    _id = models.ObjectIdField()
    productName = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    store = models.EmbeddedField(model_container=Store)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'products'

class Order(models.Model):
    _id = models.ObjectIdField()
    user = models.EmbeddedField(model_container=User)
    items = models.JSONField()
    totalCost = models.DecimalField(max_digits=10, decimal_places=2)
    shippingAddress = models.TextField()
    status = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'