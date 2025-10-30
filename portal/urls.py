from django.urls import path
from . import views

urlpatterns = [
    path('', views.beneficiary_login, name='beneficiary_login'),
    path('logout/', views.beneficiary_logout, name='beneficiary_logout'),
    path('dashboard/', views.beneficiary_dashboard, name='beneficiary_dashboard'),
    path('assets/', views.beneficiary_assets, name='beneficiary_assets'),
    path('documents/', views.beneficiary_documents, name='beneficiary_documents'),
    path('messages/', views.beneficiary_messages, name='beneficiary_messages'),
    path('help/', views.beneficiary_help, name='beneficiary_help'),
]
