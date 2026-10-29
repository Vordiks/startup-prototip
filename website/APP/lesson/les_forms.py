from django import forms
from ..models import *
'''
class Client(forms.Form):
    name = forms.CharField(label = 'Введите имя', max_length=100)
    phone = forms.CharField(label = 'Введите телефон', max_length=20)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

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
    company_name = forms.CharField(label='Название компании')
    user_login = forms.CharField(label='Логин', required=False)
    user_password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
'''