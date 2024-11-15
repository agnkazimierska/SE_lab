from django.db import models
from django.core.exceptions import ValidationError


def validatate_price_positive(value):
    if value <= 0:
        raise ValidationError('Price must be positive.')

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validatate_price_positive])
    available = models.BooleanField()


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField()


class Order(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('IN_PROCESS', 'In Process'),
        ('SENT', 'Sent'),
        ('COMPLETED', 'Completed'),
    ]

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES)

    def calculate_total_price(self):
        return sum(product.price for product in self.products.all())

    def can_be_fulfilled(self):
        return all(product.available for product in self.products.all())