from django.urls import path, include

from .views import ApiOrderList, ApiOrderDetails, ApiProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ApiProductViewSet, basename='api_product')


urlpatterns = [
    path('orders/', ApiOrderList.as_view(), name='api_order_list'),
    path('orders/<int:pk>/', ApiOrderDetails.as_view(), name='api_order_details'),
    path('', include(router.urls))
]
