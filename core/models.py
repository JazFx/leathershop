from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    minidescription = models.TextField(verbose_name='Описание', blank=True, null=True)
    price = models.IntegerField(verbose_name='Стоимость', blank=True, null=True)
    image = models.URLField(verbose_name='Фото', blank=True, null=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('infoproduct', args=[str(self.id)])

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField(verbose_name='Ссылка на изображение')

    def __str__(self):
        return f"Image for {self.product.title}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} ({self.user.username})"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    full_name = models.CharField(max_length=100, verbose_name='ФИО', blank=True, null=True)
    country = models.CharField(max_length=100, verbose_name='Страна', blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True, null=True)
    postal_code = models.CharField(max_length=20, verbose_name='Почтовый индекс', blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True, null=True)
    payment_method = models.CharField(max_length=50, verbose_name='Тип оплаты', blank=True, null=True)
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} (Order: {self.order.id})"