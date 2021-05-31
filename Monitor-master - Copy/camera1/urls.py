from django.urls import path, include
from camera1 import views

urlpatterns = [
    path('', views.indexView, name='index'),
    path('video_feed_1', views.video_feed_1, name='video_feed_1'),
]
