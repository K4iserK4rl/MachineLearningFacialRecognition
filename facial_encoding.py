from imutils import paths
import face_recognition
import pickle
import cv2
import os

#gets the paths of each file in the dataset
imagePaths = list(paths.list_images('dataset'))

knownEncodings = []
knownNames = []

#loop through image paths
for (i, imagePath) in enumerate(imagePaths):

    #Extract the name of the person from the image path
    name = imagePath.split(os.path.sep)[-2]

    #Converting image from BGR (what OpenCV uses) to RGB for dlib
    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #face_recognition used to locate faces
    faces = face_recognition.face_locations(rgb, model = 'hog')

    #Computes facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, faces)

    #Loop through encodings
    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)

#Encodings and names saved in dictionary data
data = {"Encodings: ": knownEncodings, "Names: ": knownNames}

#pickle used to save data into a file
file = open("encoded_faces", "wb")
file.write(pickle.dumps(data))
file.close()
