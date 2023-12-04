import random
import string

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def rand_slug():
    """
    Generates a random slug consisting of lowercase letters and digits.
    """
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))


class Category(models.Model):
    """
    Model representing a category of products.
    """
    name = models.CharField("Название", max_length=255, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children',
                               null=True, blank=True, verbose_name="Родительская категория")
    slug = models.SlugField("URL", max_length=250,
                            unique=True, null=False, editable=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """
        Return a string representation of the object.
        """
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        """
        Save the object to the database.
        """

        if not self.slug:
            self.slug = slugify(rand_slug() + '-pickBetter' + self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:category-list", args=[str(self.slug)])


class Product(models.Model):
    """
    Model representing a product.
    """
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField("Название", max_length=250, db_index=True)
    brand = models.CharField('Бренд', max_length=250)
    description = models.TextField("Описание", blank=True)
    slug = models.SlugField("URL", max_length=250)
    price = models.DecimalField(
        "Цена", max_digits=10, decimal_places=2, default=100.00)
    # stock = models.PositiveIntegerField("Количество")
    image = models.ImageField(
        "Изображение", upload_to='products/%Y/%m/%d', blank=True)
    available = models.BooleanField("Доступен", default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        """
        Returns a string representation of the object.
        """
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product-detail", args=[str(self.slug)])


class ProductManager(models.Manager):

    def get_queryset(self):
        """
        Retrieves the queryset for the ProductManager class.
        """
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):

    objects = ProductManager()

    class Meta:
        proxy = True
