import cv2
import face_recognition
import pickle
import imutils
import tkinter
from tkinter import filedialog
from tkinter import *

def close():
    root.destroy()

def uploadImg():
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    image.set(filename)

root = tkinter.Tk()

image = tkinter.StringVar()

button = tkinter.Button(root, text='Select Image', command=uploadImg)
button.pack()

exitButton = tkinter.Button(root, text = "Exit", command = close)
exitButton.pack()

root.mainloop()

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Loads the known facial encodings in encoded_faces file
data = pickle.loads(open('encoded_faces', "rb").read())

#Reading an image
#'dataset/Trevor/Trevor_Dog.jpg'
img = cv2.imread(image.get())

#Resizing the image
scalePercent = 30
width = int(img.shape[1] * scalePercent / 100)
height = int(img.shape[0] * scalePercent / 100)
dim = (width, height)

resizedImg = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

#Conversion from BGR to RGB
rgb = cv2.cvtColor(resizedImg, cv2.COLOR_BGR2RGB)

# Conversion to grayscale
gray = cv2.cvtColor(resizedImg, cv2.COLOR_BGR2GRAY)

#Detects faces
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor = 1.2,
    minNeighbors = 5,
    minSize = (30, 30),
    flags = cv2.CASCADE_SCALE_IMAGE
)

#Facial encodings for face(s) in the input
encodings = face_recognition.face_encodings(rgb)
names = []

#Loop through facial encodings in case of multiple faces in input
for encoding in encodings:

    #Compare encodings with encodings in data["Encodings: "]
    #Matches contain array of booleans with True for closely matching encodings
    matches = face_recognition.compare_faces(data["Encodings: "], encoding)

    #In case of no matches
    name = "Unknown"

    if True in matches:

        #Find indexes of True values and store
        matchedIndexes = [i for (i, b) in enumerate(matches) if b]
        counts = {}

        #Loop through the matches and maintain a count of recognized faces
        for i in matchedIndexes:
            #Check names at respective stored indexes
            name = data["Names: "][i]
            #Increment count
            counts[name] = counts.get(name, 0) + 1

            #Set name with highest count
            name = max(counts, key = counts.get)

        #Update list of names
        names.append(name)

        #Loop through recognized faces
        for ((x, y, w, h), name) in zip(faces, names):
            #Rectangles around the faces
            cv2.rectangle(resizedImg, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #Print predicted face name
            cv2.putText(resizedImg, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                       (0, 255, 0), 2)

    #Display Image
    cv2.imshow('img', resizedImg)

    #Press q to close the image
    if(cv2.waitKey() & 0xFF == ord('q')):
        cv2.destroyAllWindows()
