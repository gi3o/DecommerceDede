from decimal import Decimal
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from decommerce.forms import *
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from random import random


# Create your views here.
def buyer_check(user):
    return user.groups.filter(name='Buyer').exists()

def seller_check(user):
    return user.groups.filter(name='Seller').exists()

class IndexView(generic.ListView):
    template_name = 'decommerce/index.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return sorted(Product.objects.filter(added__lte=timezone.now()).order_by('-added')[:9], key=lambda x: random())


def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category, added__lte=timezone.now())
    return render(request, 'decommerce/category.html',
                  context={'actual_category': category, 'product_list': products})


@login_required
@user_passes_test(seller_check)
def add_review(request, product_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    form = ProductReviewForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        product_review = ProductReview(product=get_object_or_404(Product, pk=product_id), by=user_profile,
                                       stars=data['stars'], title=data['title'], review=data['review'])
        product_review.save()
    return HttpResponseRedirect(reverse('decommerce:product', args= [product_id]))

def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        quantity = int(request.POST['stock'])
        buyer = UserProfile.objects.get(user=request.user)
        product.decrease_stock(quantity)
        buyer.cart.create(product=product, quantity=quantity)
        return HttpResponseRedirect(reverse('decommerce:product', args=[product_id]))
    else:
        category = product.category
        reviews = ProductReview.objects.filter(product=product, date__lte=timezone.now())
        review_form = ProductReviewForm()
        context = {'actual_category': category, 'product': product,
                   'review_form': review_form, 'related_products': product.related_products(5)}
        if not request.user.is_authenticated() or SellerProfile.objects.filter(user=request.user).exists():
            context.update({'errors': ['Devi essere loggato come compratore per scrivere una recensione']})
        elif reviews.filter(by=UserProfile.objects.filter(user=request.user)).exists():
            context.update({'reviews': reviews, 'errors': ['Hai già scritto una recensione'],
                            'product_available': product.product_available})
        else:
            context.update({'reviews': reviews, 'product_available': product.product_available})
        return render(request, 'decommerce/product.html', context)

def search_term(term):
    query_set = []
    for prod in Product.objects.filter(
                Q(name__contains= term) | Q(details__contains= term) | Q(seller__store_name__contains= term)):
            query_set.append(prod)
    if Tag.objects.filter(tag= term).exists():
        tag_term = Tag.objects.get(tag= term)
        for product in Product.objects.all():
            if tag_term in product.tags.all():
                query_set.append(product)
    return list(set(query_set))


def search(request):
    if request.method == 'POST':
        query = request.POST['search']
        return render(request, 'decommerce/search.html',
                      context={'query': query, 'product_list': search_term(query), 'tag_list': Tag.objects.all().order_by('tag')})
    else:
        return render(request, 'decommerce/search_form.html')


def adv_search(request):
    if request.method == 'POST':
        query = request.POST['query']
        product_list = search_term(query)
        supp = list(product_list)
        if 'minor_price' in request.POST:
            product_list.sort(key=lambda x: x.price)
        elif 'major_price' in request.POST:
            product_list.sort(key=lambda x: x.price, reverse=True)
        elif 'best_value' in request.POST:
            product_list.sort(key=lambda x: x.stars_avg, reverse=True)
        elif 'less_value' in request.POST:
            product_list.sort(key=lambda x: x.stars_avg)
        elif 'date_time' in request.POST:
            product_list.sort(key=lambda x: x.added)
        elif 'prize_1' in request.POST:
            for prod in supp:
                if prod.price.compare_total(Decimal('10.00')) == Decimal('1'):
                    product_list.remove(prod)
        elif 'prize_2' in request.POST:
            for prod in supp:
                if ((prod.price.compare_total(Decimal('10.00')) == Decimal(-1)) or (prod.price.compare_total(Decimal('50.00')) == Decimal('1'))):
                    product_list.remove(prod)
        elif 'prize_3' in request.POST:
            for prod in supp:
                if ((prod.price.compare_total(Decimal('50.00')) == Decimal(-1)) or (prod.price.compare_total(Decimal('100.00')) == Decimal('1'))):
                    product_list.remove(prod)
        elif 'prize_4' in request.POST:
            for prod in supp:
                if ((prod.price.compare_total(Decimal('100.00')) == Decimal(-1)) or (prod.price.compare_total(Decimal('250.00')) == Decimal('1'))):
                    product_list.remove(prod)
        elif 'prize_5' in request.POST:
            for prod in supp:
                if ((prod.price.compare_total(Decimal('250.00')) == Decimal(-1)) or (prod.price.compare_total(Decimal('500.00')) == Decimal('1'))):
                    product_list.remove(prod)
        elif 'prize_6' in request.POST:
            for prod in supp:
                if ((prod.price.compare_total(Decimal('500.00')) == Decimal(-1))):
                    product_list.remove(prod)
        elif 'Elettronica' in request.POST:
            for prod in supp:
                if(prod.category != Category.objects.get(name='Elettronica')):
                    product_list.remove(prod)
        elif 'Abbigliamento' in request.POST:
            for prod in supp:
                if(prod.category != Category.objects.get(name='Abbigliamento')):
                    product_list.remove(prod)
        elif 'Musica' in request.POST:
            for prod in supp:
                if(prod.category != Category.objects.get(name='Musica')):
                    product_list.remove(prod)
        elif 'Giocattoli' in request.POST:
            for prod in supp:
                if(prod.category != Category.objects.get(name='Giocattoli')):
                    product_list.remove(prod)
        elif 'Giardinaggio' in request.POST:
            for prod in supp:
                if(prod.category != Category.objects.get(name='Giardinaggio')):
                    product_list.remove(prod)
        elif 'Libri' in request.POST:
            for prod in supp:
                if(prod.category != Category.objects.get(name='Libri')):
                    product_list.remove(prod)
        elif 'Orologi' in request.POST:
            for prod in supp:
                if(prod.category != Category.objects.get(name='Orologi')):
                    product_list.remove(prod)
        elif 'Sport' in request.POST:
            for prod in supp:
                if(prod.category != Category.objects.get(name='Sport')):
                    product_list.remove(prod)
        elif 'Strumenti Musicali' in request.POST:
            for prod in supp:
                if(prod.category != Category.objects.get(name='Strumenti Musicali')):
                    product_list.remove(prod)
        elif '1_star' in request.POST:
            for prod in supp:
                if(prod.calculateAverageVotes() >=2):
                    product_list.remove(prod)
        elif '2_star' in request.POST:
            for prod in supp:
                if((prod.calculateAverageVotes() < 2) or (prod.calculateAverageVotes() >=3)):
                    product_list.remove(prod)
        elif '3_star' in request.POST:
            for prod in supp:
                if((prod.calculateAverageVotes() < 3) or (prod.calculateAverageVotes() >=4)):
                    product_list.remove(prod)
        elif '4_star' in request.POST:
            for prod in supp:
                if ((prod.calculateAverageVotes() < 4) or    (prod.calculateAverageVotes() >= 5)):
                    product_list.remove(prod)
        elif '5_star' in request.POST:
            for prod in supp:
                if (prod.calculateAverageVotes() < 5):
                    product_list.remove(prod)
        else:
            tag_selected = ''
            for tag in Tag.objects.all():
                if tag.tag in request.POST:
                    tag_selected = tag.tag
            for prod in supp:
                if not prod.tags.all().filter(tag=tag_selected).exists():
                    product_list.remove(prod)
        return render(request, 'decommerce/search.html',
                    context={'query': query, 'product_list': product_list, 'tag_list': Tag.objects.all().order_by('tag')})
    else:
        return render(request, 'decommerce/search_form.html')


def login_view(request):
    login_form = LoginForm()
    context = {'login_form': login_form}
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('decommerce:index'))
                else:
                    context.update({'errors': ['Il tuo account è stato disabilitato']})
            else:
                context.update({'errors': ['Username o password non corretti']})
        else:
            context.update({'errors': login_form.errors})
    return render(request, 'decommerce/login.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('decommerce:index'))


def register(request):
    register_form = RegisterForm()
    context = {'register_form': register_form}
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        context.update({'register_form': register_form})
        if register_form.is_valid():
            data = register_form.cleaned_data
            if data['password'] != data['password_confirm']:
                context.update({'errors': ['Le password devono coincidere']})
                return render(request, 'decommerce/register.html', context)
            if User.objects.filter(email=data['mail']).exists():
                context.update({'errors': ['Questo indirizzo email è già in uso']})
                return render(request, 'decommerce/register.html', context)
            try:
                user = User.objects.create_user(username=data['username'], email=data['mail'],
                                                password=data['password'])
            except IntegrityError as e:
                context.update({'errors': [e.__cause__]})
                return render(request, 'decommerce/register.html', context)
            if data['type'] == 'Compratore':
                userProfile = UserProfile(user=user, nationality=data['nationality'], address=data['address'])
                userProfile.save()
                Group.objects.get(name='Buyer').user_set.add(user)
            elif data['type'] == 'Venditore':
                sellerProfile = SellerProfile(user=user, store_name=data['store_name'])
                sellerProfile.save()
                Group.objects.get(name='Seller').user_set.add(user)
            login(request, user)
            return HttpResponseRedirect(reverse('decommerce:index'))
        else:
            context.update({'errors': register_form.errors})
    return render(request, 'decommerce/register.html', context)
    
@login_required
def seller_profile(request, user, visitor=False):
    seller = SellerProfile.objects.get(user=user)
    products = Product.objects.filter(seller=seller)
    seller_reviews = SellerReview.objects.filter(seller=seller, date__lte=timezone.now())
    upload_product_form = UploadProductForm()
    seller_review_form = SellerReviewForm()
    context = {'seller': seller, 'products': products, 'seller_reviews': seller_reviews}
    template = 'decommerce/seller_profile.html'
    if request.POST:
        form = SellerReviewForm(request.POST)
        user_profile = get_object_or_404(UserProfile, user=request.user)
        if form.is_valid():
            data = form.cleaned_data
            review = SellerReview(seller=seller, by=user_profile, stars=data['stars'],
                        title=data['title'], review=data['review'])
            review.save()
        else:
            return HttpResponse(form.errors)
    if visitor:
        user_profile = UserProfile.objects.get(user=request.user)
        if SellerReview.objects.filter(by=user_profile).exists():
            context.update({'review_already_written': True, 'errors':['Hai già scritto una recensione per questo venditore']})
        context.update({'review_form': seller_review_form, 'seller_reviews':seller_reviews})
        template = 'decommerce/seller_profile_visitor.html'
    else:
        context.update({'product_form': upload_product_form})
    return render(request, template, context)


@login_required
@user_passes_test(buyer_check)
def buyer_profile(request, user):
    buyer = get_object_or_404(UserProfile, user=user)
    orders_made = Order.objects.filter(user=buyer)
    edit_user = ModifyUserDataForm(
        initial={'mail': user.email, 'name': user.first_name, 'surname': user.last_name,
                 'nationality': buyer.nationality, 'address': buyer.address})
    product_reviews_made = [review.product for review in ProductReview.objects.filter(by=buyer)]
    seller_reviews_made = [review.seller for review in SellerReview.objects.filter(by=buyer)]
    product_missing_reviews = set()
    seller_missing_reviews = set()
    for order in orders_made:
        if order.product not in product_reviews_made:
            product_missing_reviews.add(order.product)
        if order.product.seller not in seller_reviews_made:
            seller_missing_reviews.add(order.product.seller)
    context = {'buyer': buyer, 'orders': orders_made, 'edit_form': edit_user,
               'product_missing_reviews': product_missing_reviews, 'seller_missing_reviews': seller_missing_reviews}
    if request.method == "POST":
        edit_user = ModifyUserDataForm(request.POST)
        if edit_user.is_valid():
            data = edit_user.cleaned_data
            user.email = data['mail']
            user.first_name = data['name']
            user.last_name = data['surname']
            buyer.nationality = data['nationality']
            buyer.address = data['address']
            user.save()
            buyer.save()
            return HttpResponseRedirect(reverse('decommerce:profile', args= [user.id]))
        else:
            context.update({'errors': edit_user.errors})
    else:
        if user != request.user:
            return HttpResponseRedirect(reverse('decommerce:profile', args= [request.user.id]))
    return render(request, 'decommerce/buyer_profile.html', context)


@login_required
def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if UserProfile.objects.filter(user=user).exists():
        return buyer_profile(request, user)
    elif SellerProfile.objects.filter(user=user).exists():
        return seller_profile(request, user, visitor = str(request.user.id) != user_id)
    else:
        return HttpResponse('You\'re user: ' + user.get_username())


@login_required
@user_passes_test(seller_check)
def add_product(request, user_id):
    if request.method == 'POST':
        form = UploadProductForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            product = Product(name=data['name'], category=data['category'], details=data['details'],
                              price=data['price'], image=data['image'],
                              seller=get_object_or_404(SellerProfile, user=request.user), stock=data['stock'])
            product.save()
            tags = list(filter(None, data['tags'].lower().split(", ")))
            for tag in tags:
                if Tag.objects.filter(tag= tag).exists():
                    product.tags.add(Tag.objects.get(tag = tag))
                else:
                    new_tag = Tag(tag= tag)
                    new_tag.save()
                    product.tags.add(new_tag)
            product.save()
            return HttpResponseRedirect(reverse('decommerce:profile', args= [user_id]))
        else:
            return HttpResponse('Upload failed: ' + str(form.errors))
    else:
        return HttpResponseRedirect(reverse('decommerce:index'))


@login_required
@user_passes_test(seller_check)
def remove_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if SellerProfile.objects.get(user=request.user) == product.seller:
        product.delete()
    return HttpResponseRedirect(reverse('decommerce:profile', args= [request.user.id]))

@login_required
@user_passes_test(seller_check)
def edit_tags(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk= product_id)
        tags = list(filter(None, request.POST['tags'].lower().split(", ")))
        product.tags.clear()
        for tag in tags:
            if Tag.objects.filter(tag= tag).exists():
                product.tags.add(Tag.objects.get(tag= tag))
            else:
                product.tags.create(tag= tag)
    return HttpResponseRedirect(reverse('decommerce:product_details', args=[product_id]))


@login_required
@user_passes_test(seller_check)
def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    orders = Order.objects.filter(product=product)
    nations = UserProfile._meta.get_field('nationality').choices
    nations_values = [i[0] for i in nations]
    nations_orders = dict.fromkeys(nations_values, 0)
    context = {'product': product, 'orders': orders, 'nation_orders': nations_orders}
    for order in orders:
        nation = order.user.nationality
        nations_orders[nation] = nations_orders[nation] + order.quantity
    if request.method == 'POST':
        amount = int(request.POST['stock'])
        if amount > 0:
            product.increase_stock(amount)
            return HttpResponseRedirect(reverse('decommerce:product_details', args= [product_id]))
        else:
            context.update({'errors': ['Il numero di oggetti deve essere positivo']})
    return render(request, 'decommerce/product_details.html', context)


@login_required
@user_passes_test(buyer_check)
def remove_cart(request, item_id):
    if request.method == "POST":
        item = CartItem.objects.get(id=item_id)
        item.product.increase_stock(item.quantity)
        UserProfile.objects.get(user=request.user).cart.get(id=int(item_id)).delete()
    return HttpResponseRedirect(reverse('decommerce:profile', args= [request.user.id]))


@login_required
@user_passes_test(buyer_check)
def checkout(request):
    if UserProfile.objects.filter(user=request.user).exists():
        buyer = UserProfile.objects.get(user=request.user)
        for item in buyer.cart.all():
            order = Order(product=item.product, user=buyer, quantity=item.quantity)
            order.save()
            item.delete()
    return HttpResponseRedirect(reverse('decommerce:profile', args= [request.user.id]))
    
    
@login_required
@user_passes_test(buyer_check)
def compare_products(request, id_1, id_2):
    product_1 = get_object_or_404(Product, pk=id_1)
    product_2 = get_object_or_404(Product, pk=id_2)
    context = {'product_1':product_1, 'product_2':product_2}
    return render(request, 'decommerce/compare_products.html', context)
    
    
    
    
    
    
    
    
