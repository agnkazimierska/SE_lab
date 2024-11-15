from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CustomerViewSet, OrderViewSet

# urlpatterns = [
#     path('hello/', hello_world, name='hello_world'),
# ]

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'orders', OrderViewSet, basename='order')


urlpatterns = [
    path('api/', include(router.urls)),
]