import tempfile
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from decommerce.models import SellerProfile, Product, Category


# Create your tests here.

class ProductMethodTests(TestCase):
    def test_decrease_product_stock_below_zero(self):
        user = User.objects.create_user(username='testuser', email='test@test.com',
                                        password='testpassword')
        seller_profile = SellerProfile.objects.create(user=user, store_name='Test Store')
        seller_profile.save()
        category = Category(name='Test Category')
        category.save()
        product = Product(name='Test Product', category=category, price=14.5,
                          image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                          seller=seller_profile, stock=2)
        product.save()
        product.decrease_stock(10)
        product.save()
        self.assertEqual(product.stock, 0)

    def test_increase_product_stock_by_negative_number(self):
        user = User.objects.create_user(username='testuser', email='test@test.com',
                                        password='testpassword')
        seller_profile = SellerProfile.objects.create(user=user, store_name='Test Store')
        seller_profile.save()
        category = Category(name='Test Category')
        category.save()
        product = Product(name='Test Product', category=category, price=14.5,
                          image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                          seller=seller_profile, stock=2)
        product.save()
        before = product.stock
        product.increase_stock(-5)
        self.assertGreaterEqual(product.stock, before)

    def test_product_available_with_negative_stock(self):
        user = User.objects.create_user(username='testuser', email='test@test.com',
                                        password='testpassword')
        seller_profile = SellerProfile.objects.create(user=user, store_name='Test Store')
        seller_profile.save()
        category = Category(name='Test Category')
        category.save()
        product = Product(name='Test Product', category=category, price=14.5,
                          image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                          seller=seller_profile, stock=-2)
        product.save()
        self.assertEqual(product.product_available, False)

    def test_product_available_with_zero_stock(self):
        user = User.objects.create_user(username='testuser', email='test@test.com',
                                        password='testpassword')
        seller_profile = SellerProfile.objects.create(user=user, store_name='Test Store')
        seller_profile.save()
        category = Category(name='Test Category')
        category.save()
        product = Product(name='Test Product', category=category, price=14.5,
                          image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                          seller=seller_profile, stock=0)
        product.save()
        self.assertEqual(product.product_available, False)

    def test_product_tags_string_without_any_tag(self):
        user = User.objects.create_user(username='testuser', email='test@test.com',
                                        password='testpassword')
        seller_profile = SellerProfile.objects.create(user=user, store_name='Test Store')
        seller_profile.save()
        category = Category(name='Test Category')
        category.save()
        product = Product(name='Test Product', category=category, price=14.5,
                          image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                          seller=seller_profile, stock=2)
        product.save()
        self.assertEqual(product.tags_as_string, '')


class IndexViewTests(TestCase):
    def test_index_view_without_products(self):
        response = self.client.get(reverse('decommerce:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nessun prodotto disponibile')
        self.assertQuerysetEqual(response.context['product_list'], [])

    def test_index_view_with_past_products(self):
        user = User.objects.create_user(username='testuser', email='test@test.com',
                                        password='testpassword')
        seller_profile = SellerProfile.objects.create(user=user, store_name='Test Store')
        seller_profile.save()
        category = Category(name='Test Category')
        category.save()
        product = Product(name='Test Product', category=category, price=14.5,
                          image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                          seller=seller_profile, stock=10, added=timezone.now() - timedelta(days=30))
        product.save()
        response = self.client.get(reverse('decommerce:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['product_list'], ['<Product: Test Product, Test Store>'])

    def test_index_view_with_future_products(self):
        user = User.objects.create_user(username='testuser', email='test@test.com',
                                        password='testpassword')
        seller_profile = SellerProfile.objects.create(user=user, store_name='Test Store')
        seller_profile.save()
        category = Category(name='Test Category')
        category.save()
        product = Product(name='Test Product', category=category, price=14.5,
                          image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                          seller=seller_profile, stock=10, added=timezone.now() + timedelta(days=30))
        product.save()
        response = self.client.get(reverse('decommerce:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['product_list'], [])

    def test_index_view_with_mixed_products(self):
        user = User.objects.create_user(username='testuser', email='test@test.com',
                                        password='testpassword')
        seller_profile = SellerProfile.objects.create(user=user, store_name='Test Store')
        seller_profile.save()
        category = Category(name='Test Category')
        category.save()
        product = Product(name='Past Product', category=category, price=14.5,
                          image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                          seller=seller_profile, stock=10, added=timezone.now() - timedelta(days=30))
        product.save()
        product = Product(name='Future Product', category=category, price=14.5,
                          image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                          seller=seller_profile, stock=10, added=timezone.now() + timedelta(days=30))
        product.save()
        response = self.client.get(reverse('decommerce:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['product_list'], ['<Product: Past Product, Test Store>'])


class CategoryViewTests(TestCase):
    def test_non_existing_category(self):
        response = self.client.get(reverse('decommerce:category', args=[14]))
        self.assertEqual(response.status_code, 404)

    def test_category_with_no_products(self):
        category = Category(name='Test Category')
        category.save()
        response = self.client.get(reverse('decommerce:category', args=[category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nessun prodotto disponibile')
        self.assertQuerysetEqual(response.context['product_list'], [])

    def test_category_with_future_products(self):
        user = User.objects.create_user(username='testuser', email='test@test.com',
                                        password='testpassword')
        seller_profile = SellerProfile.objects.create(user=user, store_name='Test Store')
        seller_profile.save()
        category = Category(name='Test Category')
        category.save()
        product = Product(name='Future Product', category=category, price=14.5,
                          image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                          seller=seller_profile, stock=10, added=timezone.now() + timedelta(days=30))
        product.save()
        response = self.client.get(reverse('decommerce:category', args=[category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nessun prodotto disponibile')
        self.assertQuerysetEqual(response.context['product_list'], [])

    def test_category_with_past_products(self):
        user = User.objects.create_user(username='testuser', email='test@test.com',
                                        password='testpassword')
        seller_profile = SellerProfile.objects.create(user=user, store_name='Test Store')
        seller_profile.save()
        category = Category(name='Test Category')
        category.save()
        product = Product(name='Past Product', category=category, price=14.5,
                          image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                          seller=seller_profile, stock=10, added=timezone.now() - timedelta(days=30))
        product.save()
        response = self.client.get(reverse('decommerce:category', args=[category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['product_list'], ['<Product: Past Product, Test Store>'])

    def test_category_with_past_products(self):
        user = User.objects.create_user(username='testuser', email='test@test.com',
                                        password='testpassword')
        seller_profile = SellerProfile.objects.create(user=user, store_name='Test Store')
        seller_profile.save()
        category = Category(name='Test Category')
        category.save()
        product = Product(name='Past Product', category=category, price=14.5,
                          image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                          seller=seller_profile, stock=10, added=timezone.now() - timedelta(days=30))
        product.save()
        product = Product(name='Future Product', category=category, price=14.5,
                          image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                          seller=seller_profile, stock=10, added=timezone.now() + timedelta(days=30))
        product.save()
        response = self.client.get(reverse('decommerce:category', args=[category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['product_list'], ['<Product: Past Product, Test Store>'])
