import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product

# def hello_world(request):
#     return HttpResponse("Hello, World!")

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values('id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        price = data.get('price')
        available = data.get('available')

        product = Product.objects.create(
            name=name, 
            price=price,
            available=available
        )

        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
            },
            status=201
        )

def product_detail(request, product_id):
    if request.method == 'GET':
        product = Product.objects.get(id=product_id)
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
            }
        )