from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse #Отправить ответ на сервер
from ..forms import *
# Create your views here.
'''
def file_show(request):
    return FileResponse(open('.\\APP\\files\\tractor.txt', 'rb'), as_attachment=True)


def product(request):

    x = 'Hello, word!'

    return  render(request, 'product.html', {'my_variable': x})


def about(request):
    context = {
        'username':'Саша',
        'age': 30,
    }
    return  render(request, 'about.html', context)

def contact(request):
    users = [
        {'name': "Дима", 'number': '1234'},
        {'name': "Алиса", 'number': '1324'},
        {'name': "Ксюша", 'number': '4320'},
    ]
    return  render(request, 'contact.html', {'users': users})

def my_form_view(request):
    return render(request, 'my_form.html') #1


def answer_form(request):
    if request.POST:
        return HttpResponse(f'Привет {request.POST['name']}, твой телефон {request.POST['phone']}') 
    else:
        return HttpResponse(f'Привет {request.GET['name']}, твой телефон {request.GET['phone']}') #2

def form_2(request):
    form = Client()
    return render(request, 'form_2.html', {'form':form})

def model_form(req):
    if req.POST:
        form = ProductForm(req.POST)
        if form.is_valid():
            form.save()
    form = ProductForm()        
    return render(req, 'model_form.html', {'form':form})

def login_form(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)       # ← передаём данные формы
        if form.is_valid():                  # ← проверяем
            role = form.cleaned_data['manager_user']  # 'manager' или 'user'
            if role == 'manager':
                return redirect('about')
            else:
                return redirect('product')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
'''


'''
4 вебинар
def product(request, name):
    return HttpResponse(f'<h2>Имя: {name}</h2>')
'''