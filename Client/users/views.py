from django.shortcuts import render
import pyrebase

# Create your views here.

config = {
    "apiKey": "AIzaSyB9rHPXZpzCltsCYBmRUTJuAJX4gGUeI5w",
    "authDomain": "social-distance-monitoring.firebaseapp.com",
    "databaseURL": "https://social-distance-monitoring-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "social-distance-monitoring",
    "storageBucket": "social-distance-monitoring.appspot.com",
    "messagingSenderId": "601954862762",
    "appId": "1:601954862762:web:bc6f6988daa1378615b2d3",
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


def indexView(request):
    return render(request, 'home3.html')


def postSignIn(request):
    email = request.POST.get('email')
    password = request.POST.get('pass')
    try:
        # if there is no error then signin the user with given email and password
        user = authe.sign_in_with_email_and_password(email, password)
    except:
        message = "Invalid Credentials!!Please ChecK your Data"
        return render(request, "home3.html", {"message": message})
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "dashboard.html", {"email": email})
