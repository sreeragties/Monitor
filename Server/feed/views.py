from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from feed.camera1 import Camera1
from feed.camera2 import Camera2
import threading


# Create your views here.

def indexView(request):
    t1 = threading.Thread(target=Camera1)
    t2 = threading.Thread(target=Camera2)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    return render(request, 'index.html')
