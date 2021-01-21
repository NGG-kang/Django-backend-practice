
from django.urls import path

from . import views

app_name = 'pcsub'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('write/', views.write.as_view(),name='write'),
    path('write/writeBoard/', views.writeBoard, name='writeBoard'),
    path('detail/<int:pk>/', views.Detail, name='detail'),
]
