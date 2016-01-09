from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    productname = models.CharField(max_length=400)
    price = models.IntegerField()


class Machine(models.Model):
    name = models.CharField(default="brus", max_length=200)
    # meh
    product0 = models.ForeignKey(to=Product, related_name="p0", null=True)
    product1 = models.ForeignKey(to=Product, related_name="p1", null=True)
    product2 = models.ForeignKey(to=Product, related_name="p2", null=True)
    product3 = models.ForeignKey(to=Product, related_name="p3", null=True)
    product4 = models.ForeignKey(to=Product, related_name="p4", null=True)
    key = models.CharField(default="", max_length=200)


class Transaction(models.Model):
    description = models.CharField(max_length=500, blank=True)
    member = models.ForeignKey(User)
    machine = models.ForeignKey(Machine, null=True)
    value = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
