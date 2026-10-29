from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse #Отправить ответ на сервер
from .forms import *
from decimal import Decimal
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate

def test(request):
    return render(request, 'test.html')

def login_form(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)       # ← передаём данные формы
        if form.is_valid():                  # ← проверяем
            role = form.cleaned_data['manager_user']  # 'manager' или 'user'
            if role == 'manager':
                return redirect('menlog_form')
            else:
                return redirect('uslog_form')
    else:
        form = LoginForm()
    return render(request, 'LogForm.html', {'form': form})

def menlog_form(request):
    if request.method == 'POST':
        # Просто игнорируем введенные данные и пускаем в панель
        request.session['is_manager'] = True  
        return redirect('manager_home')
    
    form = ManLogForm()
    return render(request, 'LogFormMen.html', {'form': form})


def manager_home(request):
    # Проверка, что мы зашли как менеджер (чтобы не заходить через URL)
    if not request.session.get('is_manager'):
        return redirect('menlog_form')
        
    # Исключаем заявки с пустой/битой ценой
    all_purchases = purchase.objects.filter(status='new').defer('price').order_by('-created_at')
    return render(request, 'manager.html', {'purchases': all_purchases})


def update_status(request, purchase_id, new_status):
    # Проверка, что мы зашли как менеджер
    if not request.session.get('is_manager'):
        return redirect('menlog_form')
        
    item = get_object_or_404(purchase, id=purchase_id)
    if new_status in dict(purchase.STATUS_CHOICES):
        item.status = new_status
        item.save()
    return redirect('manager_home')

def uslog_form(request):
    if request.method == 'POST':
        form = UserLogForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company_name']
            request.session['company_id'] = company.id   # ← сохранили в сессию
            return redirect('homeUs')
    else:
        form = UserLogForm()
    return render(request, 'LogFormUs.html', {'form': form})

def homeUs(request):
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect('uslog_form')
        
    company = get_object_or_404(COMPANY, id=company_id)
    purchases = purchase.objects.filter(company=company).order_by('-created_at')
    
    # Безопасный подсчет общей суммы ВСЕХ заявок этой компании
    total_sum = 0
    for p in purchases:
        try:
            if p.price is not None and str(p.price).strip() != '':
                total_sum += p.price
        except Exception:
            pass
            
    # Считаем суммы по статусам (вынесли из цикла, отступы ровные)
    approved_sum = purchase.objects.filter(company=company, status='approved').aggregate(Sum('price'))['price__sum'] or 0
    new_sum = purchase.objects.filter(company=company, status='new').aggregate(Sum('price'))['price__sum'] or 0

    # Один return в конце
    return render(request, 'homeUs.html', {
        'company': company,
        'purchases': purchases,
        'total_sum': total_sum,
        'approved_sum': approved_sum,
        'new_sum': new_sum,
    })
def company_summary(request):
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect('uslog_form')
        
    company = get_object_or_404(COMPANY, id=company_id)
    
    # Считаем общую сумму всех заявок
    purchases = purchase.objects.filter(company=company)
    total_sum = 0
    for p in purchases:
        try:
            if p.price is not None and str(p.price).strip() != '':
                total_sum += p.price
        except Exception:
            pass

    # Данные для графика статусов
    approved_sum = purchase.objects.filter(company=company, status='approved').aggregate(Sum('price'))['price__sum'] or 0
    rejected_sum = purchase.objects.filter(company=company, status='rejected').aggregate(Sum('price'))['price__sum'] or 0
    new_sum = purchase.objects.filter(company=company, status='new').aggregate(Sum('price'))['price__sum'] or 0

    status_chart_data = [float(approved_sum), float(rejected_sum), float(new_sum)]
    status_chart_labels = ['Одобренные', 'Отклоненные', 'На рассмотрении']

    # Данные для линейного графика (по дням)
    daily_data = purchase.objects.filter(company=company).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        daily_sum=Sum('price')
    ).order_by('date')

    date_chart_labels = []
    date_chart_data = []
    
    for item in daily_data:
        date_chart_labels.append(item['date'].strftime('%d.%m.%Y'))
        date_chart_data.append(float(item['daily_sum']) if item['daily_sum'] else 0)

    return render(request, 'company_summary.html', {
        'company': company,
        'purchases': purchases,
        'total_sum': total_sum,
        'status_chart_labels': status_chart_labels,
        'status_chart_data': status_chart_data,
        'date_chart_labels': date_chart_labels,
        'date_chart_data': date_chart_data,
    })

def create_purchase(request):
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect('uslog_form')
    company = get_object_or_404(COMPANY, id=company_id)

    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase_obj = form.save(commit=False)
            purchase_obj.company = company
            
            selected_stocks = form.cleaned_data.get('stock_items')
            selected_products = form.cleaned_data.get('products')
            quantity = form.cleaned_data['quantity']
            
            total_price = Decimal('0.00')
            
            # ЛОГИКА ДЛЯ ТОВАРОВ СО СКЛАДА
            if selected_stocks:
                stocks_objects = Stock.objects.filter(id__in=selected_stocks)
                first_stock = stocks_objects.first()
                if first_stock:
                    total_price += first_stock.warehouse.delivery_price
                
                for stock in stocks_objects:
                    total_price += stock.product.price * quantity
                
                purchase_obj.save()
                purchase_obj.stock_items.set(stocks_objects)
                
            # ЛОГИКА ДЛЯ ТОВАРОВ У ПОСТАВЩИКА
            elif selected_products:
                products_objects = Product.objects.filter(id__in=selected_products)
                for prod in products_objects:
                    total_price += prod.price * quantity
                
                purchase_obj.save()
                purchase_obj.products.set(products_objects)
            
            else:
                purchase_obj.save()

            # Защита от пустой цены
            if not total_price:
                total_price = Decimal('0.00')
                
            purchase_obj.price = total_price
            purchase_obj.save()
            
            
            return redirect('homeUs')
            
    else:
        form = PurchaseForm()


    return render(request, 'PurchaseForm.html', {'form': form, 'company': company})

def update_status(request, purchase_id, new_status):
    # Проверка, что мы зашли как менеджер
    if not request.session.get('is_manager'):
        return redirect('menlog_form')
        
    item = get_object_or_404(purchase, id=purchase_id)
    
    # Меняем статус и сохраняем
    if new_status in dict(purchase.STATUS_CHOICES):
        item.status = new_status
        item.save()
        
    # Перенаправляем на разные страницы в зависимости от нового статуса
    if new_status == 'approved':
        return redirect('approved_purchases')
    elif new_status == 'rejected':
        return redirect('rejected_purchases')
    
    # Если статус вдруг 'new' (на рассмотрении) — возвращаем на главную
    return redirect('manager_home')


# Новая страница для одобренных
def approved_purchases(request):
    if not request.session.get('is_manager'):
        return redirect('menlog_form')
    
    # Фильтруем только одобренные
    purchases = purchase.objects.filter(status='approved').order_by('-created_at')
    return render(request, 'approved.html', {'purchases': purchases})


# Новая страница для отклоненных
def rejected_purchases(request):
    if not request.session.get('is_manager'):
        return redirect('menlog_form')
    
    # Фильтруем только отклоненные
    purchases = purchase.objects.filter(status='rejected').order_by('-created_at')
    return render(request, 'rejected.html', {'purchases': purchases})

def manager_summary(request):
    if not request.session.get('is_manager'):
        return redirect('menlog_form')
    
    # 1. Получаем данные из БД ТОЛЬКО для одобренных заявок (status='approved')
    summary_data = purchase.objects.filter(status='approved').values('company__name').annotate(
        total_requests=Count('id'),
        total_amount=Sum('price')
    ).order_by('-total_amount')
    
    # Общая сумма и количество (тоже только одобренные)
    grand_total_requests = purchase.objects.filter(status='approved').count()
    
    # Считаем общую сумму одобренных заявок (если пусто, то 0)
    grand_total_amount = purchase.objects.filter(status='approved').aggregate(Sum('price'))['price__sum'] or 0
    
    # 2. Разделяем данные на два списка для графика
    chart_labels = []
    chart_data = []
    
    for item in summary_data:
        chart_labels.append(item['company__name'])
        # Если сумма None, ставим 0, иначе переводим в число (float)
        chart_data.append(float(item['total_amount']) if item['total_amount'] else 0)
    
    # 3. Передаем все в шаблон
    return render(request, 'summary.html', {
        'summary_data': summary_data,
        'grand_total_requests': grand_total_requests,
        'grand_total_amount': grand_total_amount,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    })


