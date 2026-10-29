from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()

class Product(models.Model):
    title = models.CharField(max_length=30, default='Введите название товара',
                             verbose_name = 'Название товара', unique=True)
    brand = models.CharField(max_length=50, verbose_name='Бренд товара')
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                verbose_name='Цена товара')
    description = models.TextField(verbose_name='Описагие товара', blank = True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'