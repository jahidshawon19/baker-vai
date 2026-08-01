from django.urls import path
from . import views

app_name = 'essays'

urlpatterns = [
    path('', views.home, name='home'),
    path('essay/<int:pk>/', views.essay_detail, name='detail'),
    path('translate/', views.translate_page, name='translate'),
    path('translate/api/', views.translate_api, name='translate_api'),
]
