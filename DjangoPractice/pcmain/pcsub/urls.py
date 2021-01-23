
from django.urls import path

from . import views

app_name = 'pcsub'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('write/', views.write.as_view(), name='write'),
    path('<int:pk>/', views.Detail.as_view(), name='detail'),
    path('<int:pk>/delete', views.deleteBoard, name='delete'),
    path('<int:pk>/modify', views.Modify.as_view(), name='modify'),
    path('<int:pk>/modify/modifyBoard/', views.modifyBoard, name='modifyBoard'),
    path('write/writeBoard/', views.writeBoard, name='writeBoard'),
]
