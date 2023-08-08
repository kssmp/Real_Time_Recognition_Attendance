import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred , {
    'databaseURL' : "https://realtimefaceattendancesy-fb71d-default-rtdb.firebaseio.com/"
})

# our data
ref = db.reference('Students')
data = {
    "001" : 
    {
        "name" : "Rowan Atkinson",
        "major" : "Comedy",
        "starting_year" : 1955,
        "total_attendance" : 15,
        "standing" : "SSS",
        "year" : 15,
        "last_attendance_time" : "2022-12-11 00:54:34"
    },

    "002" : 
    {
        "name" : "Neil deGrasse Tyson",
        "major" : "Astophysics",
        "starting_year" : 1958,
        "total_attendance" : 5,
        "standing" : "A+",
        "year" : 20,
        "last_attendance_time" : "2022-12-11 00:54:34"
    },

    "003" : 
    {
        "name" : "Muhammad Ali",
        "major" : "Combat",
        "starting_year" : 1964,
        "total_attendance" : 100,
        "standing" : "A++",
        "year" : 18,
        "last_attendance_time" : "2022-12-11 00:54:34"
    }
}

# sending values of the dictionary to the database
for key,value in data.items():
    ref.child(key).set(value)