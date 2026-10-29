from django.contrib import admin
from django.urls import path
from APP.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_form, name='login_form'),
    path('user/', uslog_form, name='uslog_form'),
    path('homeUs/', homeUs, name='homeUs'),
    path('purchase/create/', create_purchase, name='create_purchase'),
    path('manager/', menlog_form, name='menlog_form'),
    path('manager/approved/', approved_purchases, name='approved_purchases'),
    path('manager/rejected/', rejected_purchases, name='rejected_purchases'), 
    path('manager/dashboard/', manager_home, name='manager_home'), 
    path('manager/status/<int:purchase_id>/<str:new_status>/', update_status, name='update_status'), # Для кнопок смены статуса
    path('manager/summary/', manager_summary, name='manager_summary'),
    path('summary/', company_summary, name='company_summary'),
    ]
