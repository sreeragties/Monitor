from django.shortcuts import render, redirect
from django.contrib import messages
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
auth = firebase.auth()
database = firebase.database()


'''def indexView(request):
    return render(request, 'index.html')'''


def loginView(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session_id = user['idToken']
            request.session['uid'] = str(session_id)
            return render(request, 'dashboard.html', {"email": email})

        except:
            messages.error(request, "Invalid Credentials!!Please Check your Data")
            return redirect('login')

    return render(request, 'index.html')
