import cv2
import os
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred , {
    'databaseURL' : "https://realtimefaceattendancesy-fb71d-default-rtdb.firebaseio.com/",
    'storageBucket' : "realtimefaceattendancesy-fb71d.appspot.com"
})


# importing student asset paths into a list 
folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList = []
studentIds = []

for path in pathList:

    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIds.append(os.path.splitext(path)[0]) # removing .png from the ids

    # replicating all the assets in the the firebase storage
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

# will generate lists with encodings for each image of the input list
def findEncodings(imagesList):
    encodeList = []

    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # face_recognition uses rgb instead of bgr that cv2 uses
        encode = face_recognition.face_encodings(img)[0] 
        encodeList.append(encode)
        
    return encodeList

encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown,studentIds]

#pickle file with encoded data as well as their ids
file = open("EncodeFile.p " , 'wb')
pickle.dump(encodeListKnownWithIds , file)
file.close()
