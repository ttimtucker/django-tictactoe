from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gridclick/', views.gridclick, name='gridclick'),
]