from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from decommerce.forms import ProductReviewForm
from .models import Category, Product, ProductReview


# Create your views here.
def index(request):
    categories = Category.objects.all()
    product_list_ord = Product.objects.order_by('-added')[:10]
    return render(request, 'decommerce/index.html',
                  context={'categories': categories, 'product_list': product_list_ord})


def category(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'decommerce/category.html',
                  context={'actual_category': category, 'categories': categories, 'product_list': products})


def product(request, product_id):
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            product_review = ProductReview(product = Product.objects.get(pk = product_id), by = request.user,
                                           stars = data['stars'], title = data['title'], review = data['review'])
            product_review.save()
            return HttpResponseRedirect('/product/' + str(product_id))
    else:
        categories = Category.objects.all()
        product = get_object_or_404(Product, pk=product_id)
        category = product.category
        reviews = ProductReview.objects.filter(product=product)
        review_form = ProductReviewForm()
        return render(request, 'decommerce/product.html',
                      context={'actual_category': category, 'categories': categories, 'product': product,
                               'reviews': reviews, 'review_form':review_form})

def search(request):
    if request.method == 'POST':
        categories = Category.objects.all()
        query = request.POST['search']
        query_set = Product.objects.filter(
            Q(name__contains=query) | Q(details__contains=query) | Q(seller__store_name__contains=query))
        return render(request, 'decommerce/search.html',
                      context={'categories': categories, 'query': query, 'product_list': query_set})
    else:
        return render(request, 'decommerce/search_form.html', context={'categories': Category.objects.all()})
