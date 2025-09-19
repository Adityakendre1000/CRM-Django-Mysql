from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.home, name='home'),
    
    # Authentication
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    
    # Contacts
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/<int:contact_id>/', views.contact_detail, name='contact_detail'),
    path('contacts/create/', views.contact_create, name='contact_create'),
    path('contacts/<int:contact_id>/edit/', views.contact_edit, name='contact_edit'),
    
    # Deals
    path('deals/', views.deal_list, name='deal_list'),
    path('deals/<int:deal_id>/', views.deal_detail, name='deal_detail'),
    path('deals/create/', views.deal_create, name='deal_create'),
    
    # Tasks
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    
    # Companies
    path('companies/', views.company_list, name='company_list'),
    path('companies/create/', views.company_create, name='company_create'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
]