from django.urls import path
from . import views

app_name = 'prediction'

urlpatterns = [
    path('', views.index, name='index'),
    path('type/<int:type_id>/', views.type_detail, name='type_detail'),
]
