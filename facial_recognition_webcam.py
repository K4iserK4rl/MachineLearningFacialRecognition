import cv2
import face_recognition
import pickle
import imutils

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Loads the known facial encodings in encoded_faces file
data = pickle.loads(open('encoded_faces', "rb").read())

videoCapture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#Window is 720x1280
videoCapture.set(3, 1280)
videoCapture.set(4, 720)

while True:
    #Frame-by-frame capture
    ret, frame = videoCapture.read()

    if(ret != 0):

        #Conversion to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Detects faces
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )

        #Conversion from BGR to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

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
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                #Print predicted face name
                cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                           (0, 255, 0), 2)

        #Display the frame
        cv2.imshow('Video', frame)

        #Press q to break the loop
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break

#Closes the webcam
videoCapture.release()
cv2.destroyAllWindows()
