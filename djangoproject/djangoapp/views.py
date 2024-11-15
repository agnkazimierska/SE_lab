from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from rest_framework.exceptions import APIException

# def hello_world(request):
#     return HttpResponse("Hello, World!")

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
