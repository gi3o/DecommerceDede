from django.contrib.auth import logout, authenticate, login
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from decommerce.forms import ProductReviewForm, LoginForm
from .models import Category, Product, ProductReview, UserProfile
from django.contrib.auth.decorators import user_passes_test, login_required


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

def check_user_profile(user):
    return user.is_authenticated() and UserProfile.objects.filter(user = user).exists()


def product(request, product_id):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return render(request, 'templates/login.html', context={'next':request.path})
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
        if reviews.filter(by = request.user).exists():
            return render(request, 'decommerce/product.html',
                        context={'actual_category': category, 'categories': categories, 'product': product,
                                'reviews': reviews, 'review_form': review_form, 'already_written': True})
        else:
            return render(request, 'decommerce/product.html',
                          context={'actual_category': category, 'categories': categories, 'product': product,
                                   'reviews': reviews, 'review_form': review_form})

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

def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            user = authenticate(username = data['username'], password = data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return render(request, 'decommerce/login.html', context={'disabled_account':True, 'form':LoginForm()})
            else:
                return render(request, 'decommerce/login.html', context={'login_error':True, 'form':LoginForm()})
    else:
        categories = Category.objects.all()
        login_form = LoginForm()
        return render(request, 'decommerce/login.html', context={'form':login_form, 'categories':categories})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
