from django.urls import path

from .views import cart_details, cart_remove, cart_add, cart_product_update

urlpatterns = [
    path('', cart_details, name='cart_details'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('update/<int:product_id>/', cart_product_update, name='cart_product_update'),
]
