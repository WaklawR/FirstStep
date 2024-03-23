from django.db import IntegrityError
from django.test import TestCase
from .models import Order, OrderItem
from shop.models import Product, Subcategory, Category


class OrderTestCase(TestCase):
    def setUp(self):
        test_category = Category.objects.create(name='TestCategory')
        test_sub_category = Subcategory.objects.create(
            name='TestSubCategory',
            category=test_category,
        )
        test_product_correct = Product.objects.create(
            name="TestProduct",
            description="TestProduct",
            price=1.0,
            stock=2,
            available=True,
            image="",
            subcategory=test_sub_category,
        )
        test_order = Order.objects.create(
            first_name="Test",
            last_name="Test",
            email="test@example.com",
            address="some-address",
            postal_code="110020",
            city="some-city",
        )
        OrderItem.objects.create(
            order=test_order,
            product=test_product_correct,
            price=test_product_correct.price,
            quantity=2,
        )

    def test_get_total_cost(self):
        test_order = Order.objects.get(first_name="Test")
        self.assertEqual(
            test_order.get_total_cost(),
            2,
        )

    def test_product_validation(self):
        test_sub_category = Subcategory.objects.get(name='TestSubCategory')
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name="TestProduct",
                description="TestProduct",
                price=-1.0,
                stock=-2,
                available=True,
                image="",
                subcategory=test_sub_category,
            )
