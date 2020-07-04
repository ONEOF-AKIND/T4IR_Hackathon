from django.urls import path
from . import views

app_name = "yolos"

urlpatterns = [
    path('', views.index, name="index"),
    path('search/', views.search, name="search"),
    path('upload/', views.upload, name="upload"),
    path('goflow/', views.goflow, name="goflow"),
]