from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from feed.camera1 import Camera1
from feed.camera2 import Camera2
import pyrebase
import threading


# Create your views here.

config={
    "apiKey": "AIzaSyB9rHPXZpzCltsCYBmRUTJuAJX4gGUeI5w",
    "authDomain": "social-distance-monitoring.firebaseapp.com",
    "databaseURL": "https://social-distance-monitoring-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "social-distance-monitoring",
    "storageBucket": "social-distance-monitoring.appspot.com",
    "messagingSenderId": "601954862762",
    "appId": "1:601954862762:web:bc6f6988daa1378615b2d3",
    
}

def indexView(request):
    t1 = threading.Thread(target=Camera1)
    t2 = threading.Thread(target=Camera2)
    t1.setDaemon(True)
    t2.setDaemon(True)
    
    return render(request, 'home3.html')

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()

def postsignIn(request):
    email=request.POST.get('email')
    pasw=request.POST.get('pass')
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"home3.html",{"message":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request,"dashboard.html",{"email":email})