from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Category, Product


# Create your views here.
def index(request):
    categories = Category.objects.all()
    product_list_ord = Product.objects.order_by('-added')[:10]
    return render(request, 'decommerce/index.html', context = {'categories':categories, 'product_list':product_list_ord})

def category(request, category_id):

    return HttpResponse("You're watching category " + str(category_id))

def product(request, product_id):
    return HttpResponse("You're watching product " + str(product_id))