from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from decommerce.forms import ProductReviewForm, LoginForm, RegisterForm, UploadProductForm, SellerReviewForm
from .models import Category, Product, ProductReview, UserProfile, SellerProfile, Order, SellerReview
from django.contrib.auth.decorators import login_required

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

@login_required
def add_review(request, product_id):
    user_profile = get_object_or_404(UserProfile, user = request.user)
    form = ProductReviewForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        product_review = ProductReview(product = get_object_or_404(Product, pk = product_id), by = user_profile,
                                           stars = data['stars'], title = data['title'], review = data['review'])
        product_review.save()
    return HttpResponseRedirect('/product/' + str(product_id))


def product(request, product_id):
    if request.method == 'POST':
        return add_review(request, product_id)
    else:
        categories = Category.objects.all()
        product = get_object_or_404(Product, pk=product_id)
        category = product.category
        reviews = ProductReview.objects.filter(product=product)
        review_form = ProductReviewForm()
        if not request.user.is_authenticated():
            return render(request, 'decommerce/product.html',
                           context={'actual_category': category, 'categories':categories, 'product': product,
                                    'review_form':review_form, 'error':'Devi essere registrato per scrivere una recensione'})
        if reviews.filter(by = UserProfile.objects.get(user = request.user)).exists():
            return render(request, 'decommerce/product.html',
                        context={'actual_category': category, 'categories': categories, 'product': product,
                                'reviews': reviews, 'review_form': review_form, 'error': 'Hai già scritto una recensione'})
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
                    return render(request, 'decommerce/login.html',
                                  context={'login_error':'Il tuo account è stato disabilitato', 'form':LoginForm()})
            else:
                return render(request, 'decommerce/login.html',
                              context={'login_error':'Username e password non corrispondono', 'form':LoginForm()})
    else:
        categories = Category.objects.all()
        login_form = LoginForm()
        return render(request, 'decommerce/login.html', context={'form':login_form, 'categories':categories})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            data = register_form.cleaned_data
            if User.objects.filter(email = data['mail']).exists():
                return render(request, 'decommerce/register.html', context={'form':register_form, 'categories':Category.objects.all(),
                        'registration_error':'Questo indirizzo email è già in uso'})
            try:
                user = User.objects.create_user(username=data['username'], email=data['mail'], password=data['password'])
            except IntegrityError as e:
                return render(request, 'decommerce/register.html', context={'form':register_form, 'categories':Category.objects.all(),
                    'registration_error':e.__cause__})
            if data['type'] == 'Compratore':
                userProfile = UserProfile(user = user, nationality= data['nationality'], address= data['address'])
                userProfile.save()
            elif data['type'] == 'Venditore':
                sellerProfile = SellerProfile(user = user, store_name = data['store_name'])
                sellerProfile.save()
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'decommerce/register.html', context={'form':register_form, 'categories':Category.objects.all(),
                'registration_error':register_form.errors})
    else:
        register_form = RegisterForm()
        categories = Category.objects.all()
        return render(request, 'decommerce/register.html', context={'form':register_form, 'categories':categories})

@login_required
def seller_profile(request, user, visitor = False):
    seller = SellerProfile.objects.get(user = user)
    products = Product.objects.filter(seller = seller)
    seller_reviews = SellerReview.objects.filter(seller = seller)
    categories = Category.objects.all()
    upload_product_form = UploadProductForm()
    seller_review_form = SellerReviewForm()
    if visitor:
        return render(request, 'decommerce/seller_profile_visitor.html',
                      context={'seller':seller, 'categories':categories, 'products':products,
                               'review_form':seller_review_form, 'seller_reviews': seller_reviews})
    else:
        return render(request, 'decommerce/seller_profile.html',
                context={'seller':seller, 'categories':categories, 'products':products,
                        'product_form':upload_product_form, 'seller_reviews':seller_reviews})
    
@login_required
def buyer_profile(request, user, visitor = False):
    buyer = get_object_or_404(UserProfile, user = user)
    return HttpResponse("You're " + user.get_username() + " you live in " + buyer.address + ", " + buyer.nationality)
       
@login_required
def profile(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    visitor = False
    if str(request.user.id) != user_id:
        visitor = True
    if UserProfile.objects.filter(user = user).exists():
        return buyer_profile(request, user, visitor)
    elif SellerProfile.objects.filter(user = user).exists():
        return seller_profile(request, user, visitor)
    else:
        return HttpResponse('You\'re user: ' + user.get_username())

@login_required
def add_product(request, user_id):
    if request.method == 'POST':
        form = UploadProductForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            product = Product(name = data['name'], category = data['category'], details = data['details'],
                              price = data['price'], image = data['image'],
                              seller = get_object_or_404(SellerProfile, user = request.user), stock = data['stock'])
            product.save()
            return HttpResponseRedirect('/account/' + str(user_id))
        else:
            return HttpResponse('Upload failed: ' + str(form.errors))
    else:
        return HttpResponseRedirect('/')

@login_required
def remove_product(request, product_id):
    product = get_object_or_404(Product, pk = product_id)
    if SellerProfile.objects.get(user = request.user) == product.seller:
        product.delete()
    return HttpResponseRedirect('/account/' + str(request.user.id))

@login_required
def product_details(request, product_id):
    product = get_object_or_404(Product, pk = product_id)
    orders = Order.objects.filter(product = product)
    nations = UserProfile._meta.get_field('nationality').choices
    nations_values = [i[0] for i in nations]
    nations_orders = dict.fromkeys(nations_values, 0)
    for order in orders:
        nation = order.user.nationality
        nations_orders[nation] = nations_orders[nation] + order.quantity
    if request.method == 'POST':
        amount = int(request.POST['stock'])
        print('Increase by', amount)
        if amount > 0:
            product.increase_stock(amount)
            return HttpResponseRedirect(request.get_full_path())
        else:
            return render(request, 'decommerce/product_details.html', 
                          context={'product':product, 'orders':orders, 'error_message':'Il numero di oggetti deve essere positivo', 'nation_orders':nations_orders})
    else:
        return render(request, 'decommerce/product_details.html', context={'product':product, 'orders':orders, 'nation_orders':nations_orders})