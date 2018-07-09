from django.urls import path
from links import views

urlpatterns = [
    path('', views.index),
    path('create_301/', views.create_301),
    path('create_302/', views.create_302),
    path('<str:custom_url>/', views.custom_url),
    path('<str:permanent_url>/chart/', views.chart)
]
