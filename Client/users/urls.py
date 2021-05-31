from django.urls import path, include
from . import views

urlpatterns = [
    #path('', views.indexView, name='index'),
    #path('login/', views.loginView, name="login"),
    path('', views.loginView, name="login")
]
