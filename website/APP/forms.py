from django import forms
from .models import *



class LoginForm(forms.Form):
    MAN_USER = [
        ('manager', 'Менеджер'),
        ('user','Пользователь')
    ]
    manager_user = forms.ChoiceField(label='Вы хотите войти как?', choices = MAN_USER)

class ManLogForm(forms.Form):
    manager_login = forms.CharField(label='Логин')
    manager_password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class UserLogForm(forms.Form):
    company_name = forms.ModelChoiceField(
        label='Название компании',
        queryset=COMPANY.objects.all(),
        empty_label='Выберите компанию',
    )
    user_login = forms.CharField(label='Логин', required=False)
    user_password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


# Вспомогательная функция для группировки товаров
def get_grouped_products():
    groups = {}
    # Проходимся по всем товарам и собираем их в словарь по категориям
    for product in Product.objects.all():
        # get_category_display() возвращает "Одежда" вместо "clothing"
        category_name = product.get_category_display() 
        if category_name not in groups:
            groups[category_name] = []
        groups[category_name].append((product.id, product.name))
    
    # Формируем список для optgroup: ("Название группы", [(id, name), ...])
    choices = []
    for category_name, items in groups.items():
        choices.append((category_name, items))
    return choices

class PurchaseForm(forms.ModelForm):
    # Выбор товаров со склада (с группировкой по складам)
    stock_items = forms.ModelMultipleChoiceField(
        queryset=Stock.objects.filter(quantity__gt=0), # Только то, что есть в наличии
        widget=forms.SelectMultiple(attrs={'size': '10'}),
        label='Выберите товары со склада (цена + доставка)',
        required=False
    )
    
    # Выбор товаров у поставщика
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.SelectMultiple(attrs={'size': '5'}),
        label='Или закажите у поставщика (дольше, но может быть дешевле)',
        required=False
    )

    class Meta:
        model = purchase
        fields = ['title', 'stock_items', 'products', 'description', 'quantity', 'link']
        labels = {
            'title': 'Название заявки',
            'description': 'Подробности',
            'quantity': 'Количество',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Группируем товары по складам, чтобы было понятно, откуда везут
        warehouse_choices = {}
        for stock in Stock.objects.filter(quantity__gt=0):
            wh = stock.warehouse
            group_name = f"Склад: {wh.name} (Доставка: {wh.delivery_price} руб., {wh.delivery_days} дн.)"
            if group_name not in warehouse_choices:
                warehouse_choices[group_name] = []
            
            warehouse_choices[group_name].append(
                (stock.id, f"{stock.product.name} — {stock.product.price} руб. (в наличии: {stock.quantity} шт.)")
            )
            
        self.fields['stock_items'].choices = [(k, v) for k, v in warehouse_choices.items()]
    # 1. Меняем тип поля на обычный MultipleChoiceField
    products = forms.MultipleChoiceField(
        choices=[],  # Заполним динамически ниже
        widget=forms.SelectMultiple(attrs={'size': '10'}), # Выпадающий список с прокруткой
        label='Выберите товары (зажмите Ctrl для выбора нескольких)',
        required=False
    )

    class Meta:
        model = purchase
        fields = ['title', 'products', 'description', 'quantity', "link"]
        labels = {
            'title': 'Что закупаем',
            'description': 'Подробности',
            'quantity': 'Количество',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 15}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 2. Группируем товары по категориям
        grouped_choices = {}
        for product in Product.objects.all():
            # Получаем красивое название категории (например, "Одежда" вместо "clothing")
            cat_name = product.get_category_display()
            if cat_name not in grouped_choices:
                grouped_choices[cat_name] = []
            # Добавляем кортеж (значение, отображаемый текст)
            grouped_choices[cat_name].append((product.id, product.name))
        
        # Преобразуем словарь в формат, понятный Django для optgroup
        choices = []
        for cat_name, items in grouped_choices.items():
            choices.append((cat_name, items))
        self.fields['products'].choices = choices
        # ВАЛИДАЦИЯ: Проверяем, что заполнено хотя бы одно поле
    def clean(self):
        cleaned_data = super().clean()
        selected_products = cleaned_data.get('products')
        link = cleaned_data.get('link')

        # Если не выбраны товары И не указана ссылка — выдаем ошибку
        if not selected_products and not link:
            raise forms.ValidationError(
                'Вы должны либо выбрать товары из списка, либо указать ссылку на товар.'
            )
        return cleaned_data