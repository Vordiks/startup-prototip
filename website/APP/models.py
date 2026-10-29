from django.db import models

# Create your models here.
class COMPANY(models.Model):
    index = models.IntegerField()
    name = models.CharField()
    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY_CHOICE = [
        ("clothing", "Одежда"),
        ("scrap", "Запчасти"),
        ("technic", "Техника"),
        ("consumables", "Расходники"),
        ("materials", "Материалы"),
        ("devices", "Приборы"),
        ("electronik", "Электроника"),
        ("other", "Прочее"),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Цена")
    times_cur = models.PositiveIntegerField(default=0, verbose_name='Срок доставки (дней)')
    img = models.ImageField(upload_to='img/', blank=True, null=True)
    decriptions = models.CharField(max_length= 1500, verbose_name='Описание', default="")

    def __str__(self):
        return f'{self.name} ({self.get_category_display()})'

class Warehouse(models.Model):
    """Наши склады в разных городах"""
    name = models.CharField(max_length=200, verbose_name='Название склада (город)')
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Стоимость доставки со склада')
    delivery_days = models.PositiveIntegerField(default=1, verbose_name='Время доставки со склада (дней)')

    def __str__(self):
        return f"{self.name} (доставка: {self.delivery_price} руб.)"

class Stock(models.Model):
    """Товары, которые уже лежат на НАШИХ складах"""
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stocks', verbose_name='Склад')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks', verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Кол-во на складе')

    def __str__(self):
        return f'{self.product.name} на складе {self.warehouse.name}'
    
class purchase(models.Model):
    STATUS_CHOICES = [
        ('new', 'На рассмотрении'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
    ]
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Итоговая цена')
    
    products = models.ManyToManyField(Product, blank=True, related_name='purchases', verbose_name='Товары (на заказ)')
    stock_items = models.ManyToManyField(Stock, blank=True, related_name='purchases', verbose_name='Товары со склада')
    
    company = models.ForeignKey(
        COMPANY,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Компания',
    )
    products = models.ManyToManyField(
        Product, 
        related_name='purchases', 
        verbose_name='Товары к закупке',
        blank=True
    )
    link = models.URLField(
        blank=True, 
        null=True, 
        verbose_name='Ссылка на товар'
    )
    title = models.CharField(max_length=200, verbose_name='Что закупаем')
    description = models.TextField(blank=True, verbose_name='Подробности')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.company.name} — {self.title} ({self.quantity} шт.)'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']   # новые сверху



