from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.loginView, name="login"),
    path('dashboard/',views.dashboardView,name="dashboard"),
    path('camera1/',views.camera1View,name="camera1"),
    path('camera2/',views.camera2View,name="camera2"),
]
