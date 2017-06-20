import tempfile

from django.contrib.auth.models import User
from django.test import TestCase
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
