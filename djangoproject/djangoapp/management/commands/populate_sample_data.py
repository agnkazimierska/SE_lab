from django.core.management.base import BaseCommand
from djangoapp.models import Product, Customer, Order

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        product1 = Product.objects.create(
            name='Test product 1',
            price=9.99,
            available=True
        )

        product2 = Product.objects.create(
            name='Test product 2',
            price=1.99,
            available=True
        )

        product3 = Product.objects.create(
            name='Test product 3',
            price=5,
            available=False
        )

        customer1 = Customer.objects.create(
            name='Test customer 1',
            address='Xxx 123'
        )

        customer2 = Customer.objects.create(
            name='Test customer 2',
            address='Yyy 456'
        )

        customer3 = Customer.objects.create(
            name='Test customer 3',
            address='Zzz 789'
        )

        order1 = Order.objects.create(
            customer=customer1,
            status='NEW'
        )
        order1.products.add(product1)

        order2 = Order.objects.create(
            customer=customer2,
            status='IN_PROCESS'
        )
        order2.products.add(product1)
        order2.products.add(product2)

        order3 = Order.objects.create(
            customer=customer2,
            status='COMPLETED'
        )
        order3.products.add(product3)

        self.stdout.write('Data created successfully.')


