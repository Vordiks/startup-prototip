from django.contrib import admin
from django.urls import path, include
from APP.views import *

'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product, name='product'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('test/', file_show, name = "test"),
    ##############################################

    path('my_form/', my_form_view, name='my_form'), #1
    path('answer_form/', answer_form, name='answer_form'),
    path('form2/', form_2, name='form_2'),
    path('modelform/', model_form, name='model_form'),
    path('loginform/', login_form, name='login_form'),
]

4 вебинар
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('user/<name>/', product)
]
'''