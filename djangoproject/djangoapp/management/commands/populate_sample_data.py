from django.core.management.base import BaseCommand
from djangoapp.models import Product, Customer, Order
from decimal import Decimal

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        product1 = Product(name='Test product 1', price=Decimal('9.99'), available=True)
        product1.full_clean()
        product1.save()

        product2 = Product(name='Test product 2', price=Decimal('1.99'), available=True)
        product2.full_clean()
        product2.save()

        product3 = Product(name='Test product 3', price=Decimal('5.00'), available=False)
        product3.full_clean()
        product3.save()

        customer1 = Customer(name='Test customer 1', address='Xxx 123')
        customer1.full_clean()
        customer1.save()

        customer2 = Customer(name='Test customer 2', address='Yyy 456')
        customer2.full_clean()
        customer2.save()

        customer3 = Customer(name='Test customer 3', address='Zzz 789')
        customer3.full_clean()
        customer3.save()

        order1 = Order(customer=customer1, status='NEW')
        order1.full_clean()
        order1.save()

        order1.products.add(product1)

        order2 = Order(customer=customer2, status='IN_PROCESS')
        order2.full_clean()
        order2.save()
        
        order2.products.add(product1)
        order2.products.add(product2)

        order3 = Order(customer=customer2, status='COMPLETED')
        order3.full_clean()
        order3.save()

        order3.products.add(product3)

        self.stdout.write('Data created successfully.')


