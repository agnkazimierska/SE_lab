from django.test import TestCase
from djangoapp.models import Product, Customer, Order
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError, DataError
from decimal import Decimal

class ProductModelTest(TestCase):

    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(name='Temporary product', price=1.99, available=True)
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_name_missing(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(price=1.99, available=True)
            temp_product.full_clean()

    def test_create_product_with_price_missing(self):
        with self.assertRaises(IntegrityError):
            temp_product = Product.objects.create(name='Invalid product', available=True)
            temp_product.full_clean()

    def test_create_product_with_available_missing(self):
        with self.assertRaises(IntegrityError):
            temp_product = Product.objects.create(name='Invalid product', price=1.99)
            temp_product.full_clean()

    def test_create_product_with_name_blank(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='', price=0.01, available=True)
            temp_product.full_clean()

    def test_create_product_with_near_maximum_name_length(self):
        long_name = 'X' * 254
        temp_product = Product.objects.create(name=long_name, price=1.99, available=True)
        self.assertEqual(temp_product.name, long_name)
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_maximum_name_length(self):
        long_name = 'X' * 255
        temp_product = Product.objects.create(name=long_name, price=1.99, available=True)
        self.assertEqual(temp_product.name, long_name)
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_name_exceeding_maximum_length(self):
        long_name = 'X' * 256
        with self.assertRaises(DataError):
            temp_product = Product.objects.create(name=long_name, price=1.99, available=True)
            temp_product.full_clean()

    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Invalid product', price=-0.01, available=True)
            temp_product.full_clean()

    def test_create_product_with_zero_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Invalid product', price=0.0, available=True)
            temp_product.full_clean()

    def test_create_product_with_minimum_positive_price(self):
        temp_product = Product.objects.create(name='Valid product', price=0.01, available=True)
        self.assertEqual(temp_product.name, 'Valid product')
        self.assertEqual(temp_product.price, 0.01)
        self.assertTrue(temp_product.available)

    def test_create_product_with_near_maximum_positive_price(self):
        large_price = 10**8 - 0.02
        temp_product = Product.objects.create(name='Valid product', price=large_price, available=True)
        self.assertEqual(temp_product.name, 'Valid product')
        self.assertEqual(temp_product.price, large_price)
        self.assertTrue(temp_product.available)

    def test_create_product_with_maximum_positive_price(self):
        large_price = 10**8 - 0.01
        temp_product = Product.objects.create(name='Valid product', price=large_price, available=True)
        self.assertEqual(temp_product.name, 'Valid product')
        self.assertEqual(temp_product.price, large_price)
        self.assertTrue(temp_product.available)

    def test_create_product_with_price_exceeding_maximum(self):
        large_price = 10**8
        with self.assertRaises(DataError):
            temp_product = Product.objects.create(name='Invalid product', price=large_price, available=True)
            temp_product.full_clean()

    def test_create_product_with_invalid_price_decimal_places(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Invalid product', price=0.003, available=True)
            temp_product.full_clean()

            
class CustomerModelTest(TestCase):

    def test_create_customer_with_valid_data(self):
        temp_customer = Customer.objects.create(name='Temporary customer', address='123 Xyz Abc')
        self.assertEqual(temp_customer.name, 'Temporary customer')
        self.assertEqual(temp_customer.address, '123 Xyz Abc')

    def test_create_customer_with_name_missing(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer.objects.create(address='123 Xyz Abc')
            temp_customer.full_clean()

    def test_create_customer_with_address_missing(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer.objects.create(name='Invalid customer')
            temp_customer.full_clean()

    def test_create_customer_with_name_blank(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer.objects.create(name='', address='123 Xyz Abc')
            temp_customer.full_clean()

    def test_create_customer_with_address_blank(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer.objects.create(name='Invalid customer', address='')
            temp_customer.full_clean()

    def test_create_customer_with_near_maximum_name_length(self):
        long_name = 'X' * 99
        temp_customer = Customer.objects.create(name=long_name, address='123 Xyz Abc')
        self.assertEqual(temp_customer.name, long_name)
        self.assertEqual(temp_customer.address, '123 Xyz Abc')

    def test_create_customer_with_maximum_name_length(self):
        long_name = 'X' * 100
        temp_customer = Customer.objects.create(name=long_name, address='123 Xyz Abc')
        self.assertEqual(temp_customer.name, long_name)
        self.assertEqual(temp_customer.address, '123 Xyz Abc')

    def test_create_product_with_name_exceeding_maximum_length(self):
        long_name = 'X' * 101
        with self.assertRaises(DataError):
            temp_customer = Customer.objects.create(name=long_name, address='123 Xyz Abc')
            temp_customer.full_clean()


class OrderModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(name='Temporary Customer', address='123 Xyz Abc')
        self.product1 = Product.objects.create(name='Temporary Product 1', price=1.00, available=True)
        self.product2 = Product.objects.create(name='Temporary Product 2', price=4.99, available=True)
        self.product3 = Product.objects.create(name='Temporary Product 3', price=12.35, available=False)

    def test_create_order_with_valid_data(self):
        temp_order = Order.objects.create(customer=self.customer, status='NEW')
        temp_order.products.add(self.product1, self.product2)

        self.assertEqual(temp_order.customer, self.customer)
        self.assertEqual(temp_order.status, 'NEW')
        self.assertIn(self.product1, temp_order.products.all())
        self.assertIn(self.product2, temp_order.products.all())

    def test_create_order_with_customer_missing(self):
        with self.assertRaises(IntegrityError):
            temp_order = Order.objects.create(status='NEW')
            temp_order.full_clean()
        
    def test_create_order_with_status_missing(self):
        with self.assertRaises(ValidationError):
            temp_order = Order.objects.create(customer=self.customer)
            temp_order.full_clean()

    def test_create_order_with_status_invalid(self):
        with self.assertRaises(ValidationError):
            temp_order = Order.objects.create(customer=self.customer, status='INVALID')
            temp_order.full_clean()

    def test_calculate_total_price_positive(self):
        temp_order = Order.objects.create(customer=self.customer, status='NEW')
        temp_order.products.add(self.product1, self.product2)
        self.assertEqual(temp_order.calculate_total_price(), Decimal('5.99'))

    def test_calculate_total_price_zero(self):
        temp_order = Order.objects.create(customer=self.customer, status='NEW')
        self.assertEqual(temp_order.calculate_total_price(), 0)

    def test_can_be_fulfilled_true(self):
        temp_order = Order.objects.create(customer=self.customer, status='NEW')
        temp_order.products.add(self.product1, self.product2)
        self.assertTrue(temp_order.can_be_fulfilled())

    def test_can_be_fulfilled_false(self):
        temp_order = Order.objects.create(customer=self.customer, status='NEW')
        temp_order.products.add(self.product1, self.product3)
        self.assertFalse(temp_order.can_be_fulfilled())