import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import Product
from decimal import Decimal

# def hello_world(request):
#     return HttpResponse("Hello, World!")

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values('id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)

        if 'name' not in data or 'price' not in data or 'available' not in data:
            return HttpResponseBadRequest('Missing required fields.')

        name = data.get('name')
        price = data.get('price')
        available = data.get('available')

        try:
            product = Product(name=name, price=Decimal(str(price)), available=available)
            product.full_clean()
            product.save()

            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'available': product.available
                },
                status=201
            )
        except ValidationError:
            return HttpResponseBadRequest('Invalid data.')
    return HttpResponseBadRequest(f'Method {request.method} not allowed on this endpoint.')

@csrf_exempt
def product_detail(request, product_id):
    try:
        if request.method == 'GET':
            product = Product.objects.get(id=product_id)
            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'available': product.available
                }
            )
    except Product.DoesNotExist:
        return HttpResponseNotFound(f'Product {product_id} not found.')
    return HttpResponseBadRequest(f'Method {request.method} not allowed on this endpoint.')