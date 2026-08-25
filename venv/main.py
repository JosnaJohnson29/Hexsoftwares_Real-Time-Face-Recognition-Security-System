import cv2
import os
import pickle
import numpy as np
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
  "databaseURL":"https://faceattendancerealtimebyjo-default-rtdb.firebaseio.com/"

})

cap = cv2.videoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("Resources/background.png")

folderModePath = cv2.imread("Resources/background.png")

# importing the mode image into a list

folderModePath = "Resources/Modes"
modePathList = os.listdir(folderModePath)

importList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath_path)))

# print(len(imgModeList))

# Load the encoding file

print("Loading Encode File ...")
file = open("EncodeFile.p" , "rb")
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
#print(studentIds)
print("Encode File Loaded")

modeType = 0
counter = 0

while True:
    success, img = cap.read()

    imgs = cv2.resize(img,(0.0), None, 0.25, 0.25)
    imgs = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_Locations(imgs)
    encodeCurFrame = face_recognition.face_encoding(imgs, faceCurFrame)


    imgBackground[162:162+480,55:55+640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[0]

    for encodeFace, faceLoc in zip (encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print("matches", matches)
        #print("faceDis", faceDis)


        matchIndex = np.argmin(faceDis)
        #print("Match Index", matchIndex)

        if matches(matchIndex):
            #print("Know Face Detected")
            #print(studentIds[matchIndex])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4,x2 * 4,y2 * 4,x1 * 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            imgBackground = cvZone.cornerRect(imgBackground, bbox, rt = 0)
            id = studentIds[matchIndex]

        if counter == 0:
            counter = 1  

        if counter != 0:

            if counter == 1:
                # Get the Data  
                studentInfo = db.reference(f"students/{id}").get()
                print(studentInfo)   

                cv2.putText(imgBackground,str(studentInfo["total_attendence"]), (861,125))
                cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1
                cv2.putText(imgBackground,str(studentInfo["name"]), (808,445))
                cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1 
                cv2.putText(imgBackground,str(studentInfo["major"]), (1006,550))
                cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1 
                cv2.putText(imgBackground,str(id), (1006,493))
                cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1 
                cv2.putText(imgBackground,str(studentInfo["standing"]), (910,625))
                cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1
                cv2.putText(imgBackground,str(studentInfo["year"]), (1025,625))
                cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1
                cv2.putText(imgBackground,str(studentInfo["starting_year"]), (1125,625))
                cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1   




    # cv2.imshow("webcam", img)
    cv2.imshow("face Attendence", imgBackground)
    cv2.waitKey(1)