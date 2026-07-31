from django.urls import path
from . import views

app_name = 'essays'

urlpatterns = [
    path('', views.home, name='home'),
    path('essay/<int:pk>/', views.essay_detail, name='detail'),
]
