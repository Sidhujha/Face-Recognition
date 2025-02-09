import cv2
import numpy as np
from PIL import Image
import os

#path for face image database
path='Dataset'
recognizer=cv2.face.LBPHFaceRecognizer_create()
detector=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

#function to get the image and label data
def getImagesAndLabels(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    faceSamples=[]
    ids=[]

    for imagePath in imagePaths:
        PIL_img=Image.open(imagePath).convert('L')  #convert it in grayscale
        img_numpy=np.array(PIL_img,'uint8')

        id=int(os.path.split(imagePath)[-1].split(".")[1])
        faces=detector.detectMultiScale(img_numpy)

        for(x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
        
    return faceSamples,ids

print("\n [INFO] training faces. It will take a few seconds. wait...")
faces,ids=getImagesAndLabels(path)
recognizer.train(faces,np.array(ids))

#save the model into trainer/trainer.yml
recognizer.write('Trainer/trainer.yml') #recognizer.save() worked on Mac,but not on Pi

#print the number of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting program".format(len(np.unique(ids))))