from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique= True, blank= False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('category')
        
NATION_CHOICES = [('ITA', 'Italia'),
                  ('ENG', 'Ingilterra'),
                  ('USA', 'Stati Uniti'),
                  ('FRA', 'Francia'),
                  ('SPA', 'Spagna')]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nationality = models.CharField(max_length=3, validators=[MinLengthValidator(3)], choices = NATION_CHOICES)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.user.get_username()

    class Meta:
        verbose_name = _('user profile')

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    store_name = models.CharField(max_length=40, unique= True, blank= False)

    def __str__(self):
        return self.store_name

    class Meta:
        verbose_name = _('seller profile')

def content_file_name(instance, filename):
    return '/'.join(['photos', str(instance.seller.user), get_random_string(length=32)])

class Product(models.Model):
    name = models.CharField(max_length=100, blank= False)
    category = models.ForeignKey(Category, blank= False)
    details = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)], blank= False)
    image = models.ImageField(blank= False, upload_to=content_file_name)
    seller = models.ForeignKey(SellerProfile, blank= False)
    stock = models.PositiveIntegerField()
    added = models.DateTimeField(default= timezone.now)

    def __str__(self):
        return self.name + ", " + self.seller.store_name

    class Meta:
        verbose_name = _('product')
        
STAR_CHOICES=[(1, '1'),
         (2, '2'),
         (3, '3'),
         (4, '4'),
         (5, '5')]

class SellerReview(models.Model):
    seller = models.ForeignKey(SellerProfile)
    by = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    stars = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], choices = STAR_CHOICES)
    review = models.TextField()

    def __str__(self):
        return self.seller.store_name + ", " + self.by.user.get_username() + ", " + str(self.stars) + " stars"

    class Meta:
        verbose_name = _('seller review')

class Order(models.Model):
    product = models.ForeignKey(Product)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.product.name + ", " + self.user.user.get_username() + ", " + self.quantity

    class Meta:
        verbose_name = _('order')

class ProductReview(models.Model):
    product = models.ForeignKey(Product)
    by = models.OneToOneField(User, on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], choices = STAR_CHOICES)
    title = models.CharField(max_length= 30, blank= False)
    review = models.CharField(max_length= 280)

    def __str__(self):
        return self.product.name + ", " + str(self.stars) + " stars"

    class Meta:
        verbose_name = _('product review')
