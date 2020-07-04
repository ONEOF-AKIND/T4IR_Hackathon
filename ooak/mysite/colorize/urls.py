from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "colorizes"

urlpatterns = [
    path('index', views.index, name = "index"),
    path('upload/', views.upload,name = "upload"),
    path('upload2/', views.upload2,name = "upload2"),
    path('colorize/',views.colorize,name="colorize"),
    # path('search/', views.search, name = "search")
]