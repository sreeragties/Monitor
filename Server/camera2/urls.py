from django.urls import path, include
from camera2 import views

urlpatterns = [
    path('', views.indexView, name='index'),
    path('video_feed_2', views.video_feed_2, name='video_feed_2'),
]
