import sys
import os
import tkinter

#Creates root window
root = tkinter.Tk()
root.title('Facial Recognition GUI')
root.iconbitmap('face-recognition.ico')

#Set window size
root.geometry("500x200")

#Picture button
def pictureCall():
    os.system('facial_recognition_picture.py')

pictureButton = tkinter.Button(root, text = "Picture", command = pictureCall)
pictureButton.pack()

#Webcam button
def webcamCall():
    os.system('facial_recognition_webcam.py')

webcamButton = tkinter.Button(root, text = "Webcam", command = webcamCall)
webcamButton.pack()

#Image scraping button
def imageScrapeCall():
    os.system('image_web_scraper.py')

imageScrapeButton = tkinter.Button(root, text = "Scrape Images", command = imageScrapeCall)
imageScrapeButton.pack()

#Encode Faces button
def encodeFacesCall():
    os.system('facial_encoding.py')

encodeFacesButton = tkinter.Button(root, text = "Encode Faces", command = encodeFacesCall)
encodeFacesButton.pack()

#Exit button
def close():
    root.destroy()

exitButton = tkinter.Button(root, text = "Exit", command = close)
exitButton.pack()

#Runs the GUI
root.mainloop()
