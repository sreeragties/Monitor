import pyrebase

config={
    "apiKey": "AIzaSyB9rHPXZpzCltsCYBmRUTJuAJX4gGUeI5w",
    "authDomain": "social-distance-monitoring.firebaseapp.com",
    "projectId": "social-distance-monitoring",
    "databaseURL":"https://social-distance-monitoring-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "social-distance-monitoring.appspot.com",
    "messagingSenderId": "601954862762",
    "appId": "1:601954862762:web:bc6f6988daa1378615b2d3",
    "measurementId": "G-VTWHBJ84FW"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()
storage = firebase.storage()
user = auth.sign_in_with_email_and_password("sdistancemonitoring@gmail.com", "Sdistance@cs8a")