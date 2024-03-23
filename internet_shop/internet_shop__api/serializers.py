from rest_framework import serializers
from orders.models import Order

from shop.models import Product


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'address',
            'date_created',
            'paid',
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'stock',
            'price',
            'available',
            'date_created',
            'subcategory',
        ]

