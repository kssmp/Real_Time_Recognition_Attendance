import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred , {
    'databaseURL' : "https://realtimefaceattendancesy-fb71d-default-rtdb.firebaseio.com/",
    'storageBucket' : "realtimefaceattendancesy-fb71d.appspot.com"
})

bucket = storage.bucket()

modeType = 0
counter = 0 # counter used so that we only download the data form the databse once
id = -1 # for when we want the id of the face that gets matched
imgStudent = []

cap = cv2.VideoCapture(0)
# 640 x 480 size
cap.set(3, 640)
cap.set(4, 480)

# graphics
imgBackground = cv2.imread('Resources/background.png')

# importing asset paths into a list 
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))

# Loading the encoded pickle
file = open('/Users/saketprasad/Desktop/Face Recognition/EncodeFile.p ' , 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown , studentIds = encodeListKnownWithIds


while True:
    success, img = cap.read()

    imgS = cv2.resize(img , (0,0) , None , 0.25 , 0.25) # resizing the image as the using the whole image will imcrease computational complexity
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    faceCurrFrame = face_recognition.face_locations(imgS) #location of the face
    encodeCurrFrame = face_recognition.face_encodings(imgS , faceCurrFrame) # making the encodings for the current face

    imgBackground[162:162 + 480 , 55:55 + 640] = img # overlaying the two images on top
    imgBackground[44:44 + 633 , 808:808 + 414] = imgModeList[modeType]

    if faceCurrFrame : 
        #encodeFace is our curr new face
        for encodeFace , faceLoc in zip(encodeCurrFrame,faceCurrFrame):
            matches = face_recognition.compare_faces(encodeListKnown , encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown , encodeFace) # lower the face distance better the match is

            matchIndex = np.argmin(faceDis) # getting index of the matched face

            if matches[matchIndex]:
                y1,x2,y2,x1 = faceLoc # for the bounding box  -> bbox
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4 # as we resized it down by 1/4th
                bbox = 55+x1 , 162+y1 , x2-x1 , y2-y1 # the sequence is x1 y1 height width
                imgBackground = cvzone.cornerRect(imgBackground, bbox , rt = 0)
                id  = studentIds[matchIndex]
                    
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading" , (275,400))
                    cv2.imshow("Face Attendance" , imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0 :

            if counter == 1: # accessing our database for the first frame only

                # getting the data
                studentInfo = db.reference(f'Students/{id}').get() 

                # getting the images
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(),np.uint8)
                imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

                #updating the data for attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                    "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                if secondsElapsed > 30 :
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633 , 808:808 + 414] = imgModeList[modeType]


            if modeType != 3 :
                if 100 < counter < 200:
                    modeType = 2
                    imgBackground[44:44 + 633 , 808:808 + 414] = imgModeList[modeType]

                if counter <= 100 :
                    #putting the text in the right place and css formating
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']) , (862,125) , 
                                cv2.FONT_HERSHEY_COMPLEX , 1 , (255,255,255) , 1)

                    cv2.putText(imgBackground, str(studentInfo['major']) , (1006,550) , 
                                cv2.FONT_HERSHEY_COMPLEX , 0.5 , (255,255,255) , 1) # 0.5 is the size
                    
                    cv2.putText(imgBackground, str(id) , (1006,493) , 
                                cv2.FONT_HERSHEY_COMPLEX , 0.5 , (255,255,255) , 1)
                    
                    cv2.putText(imgBackground, str(studentInfo['standing']) , (910,625) , 
                                cv2.FONT_HERSHEY_COMPLEX , 0.6 , (100,100,100) , 1)
                    
                    cv2.putText(imgBackground, str(studentInfo['year']) , (1025,625) , 
                                cv2.FONT_HERSHEY_COMPLEX , 0.6 , (100,100,100) , 1)
                    
                    cv2.putText(imgBackground, str(studentInfo['starting_year']) , (1125,625) , 
                                cv2.FONT_HERSHEY_COMPLEX , 0.6 , (100,100,100) , 1)

                    (w , h) , _ = cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX , 1 , 1)        
                    offset = (414 - w)//2
                    cv2.putText(imgBackground, str(studentInfo['name']) , (808+offset,445) , 
                                cv2.FONT_HERSHEY_COMPLEX , 1 , (50,50,50) , 1)
                    
                    imgBackground[175 : 175+216 , 909:909+216] = imgStudent

                counter += 1

                if counter >= 200:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633 , 808:808 + 414] = imgModeList[modeType]
    else :
        modeType = 0
        counter = 0
    cv2.imshow("Background" , imgBackground)
    
    cv2.waitKey(1) # 1 milisecond delay
