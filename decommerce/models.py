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

    def calculateAverageVotes(self):
        reviews = SellerReview.objects.filter(seller= self)
        if not reviews.exists():
            return -1
        sum = 0
        for rev in reviews:
            sum += rev.stars
        return sum/reviews.count()

    star_avg = property(calculateAverageVotes)

    class Meta:
        verbose_name = _('seller profile')

def content_file_name(instance, filename):
    return '/'.join(['photos', instance.seller.user.username, get_random_string(length=32)])

class Product(models.Model):
    name = models.CharField(max_length=100, blank= False)
    category = models.ForeignKey(Category, blank= False, on_delete= models.CASCADE)
    details = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)], blank= False)
    image = models.ImageField(blank= False, upload_to=content_file_name)
    seller = models.ForeignKey(SellerProfile, blank= False, on_delete= models.CASCADE)
    stock = models.PositiveIntegerField()
    added = models.DateTimeField(default= timezone.now)

    def __str__(self):
        return self.name + ", " + self.seller.store_name

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(Product, self).delete(*args, **kwargs)
        storage.delete(path)

    def decrease_stock(self, quantity):
        if quantity < self.stock:
            self.stock -= quantity

    def increase_stock(self, quantity):
        self.stock += quantity
        self.save()

    def calculateAverageVotes(self):
        reviews = ProductReview.objects.filter(product = self)
        if not reviews.exists():
            return -1
        sum = 0
        for rev in reviews:
            sum += rev.stars
        return sum/reviews.count()

    stars_avg = property(calculateAverageVotes)

    class Meta:
        verbose_name = _('product')
        
STAR_CHOICES=[(1, '1'),
         (2, '2'),
         (3, '3'),
         (4, '4'),
         (5, '5')]

class SellerReview(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete= models.CASCADE)
    by = models.OneToOneField(UserProfile, null= True, on_delete= models.SET_NULL)
    stars = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], choices = STAR_CHOICES)
    title = models.CharField(max_length= 30, blank= False)
    review = models.TextField()
    date = models.DateTimeField(default= timezone.now)

    def __str__(self):
        return self.seller.store_name + ", " + str(self.by) + ", " + str(self.stars) + " stars"

    class Meta:
        verbose_name = _('seller review')

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    user= models.ForeignKey(UserProfile)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.product.name + ", " + str(self.user) + ", " + str(self.quantity)

    class Meta:
        verbose_name = _('order')

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    by = models.OneToOneField(UserProfile, null = True, on_delete= models.SET_NULL)
    stars = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], choices = STAR_CHOICES)
    title = models.CharField(max_length= 30, blank= False)
    review = models.CharField(max_length= 280)
    date = models.DateTimeField(default= timezone.now)

    def __str__(self):
        return self.product.name + ", " + str(self.stars) + " stars"

    class Meta:
        verbose_name = _('product review')
