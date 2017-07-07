from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('category')


NATION_CHOICES = [('ITA', 'Italia'),
                  ('ENG', 'Inghilterra'),
                  ('USA', 'Stati Uniti'),
                  ('FRA', 'Francia'),
                  ('SPA', 'Spagna')]


def content_file_name(instance, filename):
    return '/'.join(['photos', instance.seller.user.username, get_random_string(length=32)])


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    store_name = models.CharField(max_length=40, unique=True, blank=False)

    def __str__(self):
        return self.store_name

    def calculateAverageVotes(self):
        reviews = SellerReview.objects.filter(seller=self)
        if not reviews.exists():
            return -1
        sum = 0
        for rev in reviews:
            sum += rev.stars
        return sum / reviews.count()

    star_avg = property(calculateAverageVotes)

    class Meta:
        verbose_name = _('seller profile')


class Tag(models.Model):
    tag = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.tag


class Product(models.Model):
    name = models.CharField(max_length=100, blank=False)
    category = models.ForeignKey(Category, blank=False, on_delete=models.CASCADE)
    details = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)], blank=False)
    image = models.ImageField(blank=False, upload_to=content_file_name)
    seller = models.ForeignKey(SellerProfile, blank=False, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    added = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name + ", " + self.seller.store_name

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(Product, self).delete(*args, **kwargs)
        storage.delete(path)

    def decrease_stock(self, quantity):
        if quantity <= self.stock:
            self.stock -= quantity
        else:
            self.stock = 0
        self.save()

    def increase_stock(self, quantity):
        if quantity > 0:
            self.stock += quantity
        self.save()

    def calculateAverageVotes(self):
        reviews = ProductReview.objects.filter(product=self)
        if not reviews.exists():
            return -1
        else:
            return sum([rev.stars for rev in reviews]) / reviews.count()

    stars_avg = property(calculateAverageVotes)

    def productAvailable(self):
        return self.stock > 0

    product_available = property(productAvailable)

    def tags_as_string(self):
        return ", ".join([tag.tag for tag in self.tags.all()])

    tags_as_string = property(tags_as_string)

    def related_products(self, number):
        product_tags_set = set(self.tags.all())
        related_products = [prod for prod in Product.objects.filter(category=self.category).exclude(pk=self.id)]
        related_products.sort(key=lambda x: product_tags_set.intersection(x.tags.all()))
        return related_products[:number]

    class Meta:
        verbose_name = _('product')


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nationality = models.CharField(max_length=3, validators=[MinLengthValidator(3)], choices=NATION_CHOICES)
    address = models.CharField(max_length=50)
    cart = models.ManyToManyField(CartItem)

    def __str__(self):
        return self.user.get_username()

    def cartTotal(self):
        return sum([item.product.price * item.quantity for item in self.cart.all()])

    cart_total = property(cartTotal)

    class Meta:
        verbose_name = _('user profile')


STAR_CHOICES = [(1, '1'),
                (2, '2'),
                (3, '3'),
                (4, '4'),
                (5, '5')]


class SellerReview(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    by = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    stars = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], choices=STAR_CHOICES)
    title = models.CharField(max_length=30, blank=False)
    review = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.seller.store_name + ", " + str(self.by) + ", " + str(self.stars) + " stars"

    class Meta:
        verbose_name = _('seller review')
        unique_together = ('seller', 'by')


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product.name + ", " + str(self.user) + ", " + str(self.quantity)

    class Meta:
        verbose_name = _('order')


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    by = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    stars = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], choices=STAR_CHOICES)
    title = models.CharField(max_length=30, blank=False)
    review = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product.name + ", " + str(self.stars) + " stars"

    class Meta:
        verbose_name = _('product review')
        unique_together = ('product', 'by')
