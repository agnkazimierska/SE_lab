from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

# urlpatterns = [
#     path('hello/', hello_world, name='hello_world'),
# ]

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('api/', include(router.urls)),
]