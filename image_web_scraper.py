import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import io
import requests
import PIL.Image
import os
import hashlib
import tkinter
from tkinter import *

#def close():
    #root.destroy()

#def takeInput():
    #sT_Input.get() #= sT_Box.get("1.0", "end-1c")
    #nL_Input.get() #= nL_Box.get("1.0", "end-1c")

#root = tkinter.Tk()

#sT_Input = tkinter.StringVar()
#nL_Input = tkinter.IntVar()

#sT = Label(text = "What would you like images of in the dataset: ")

#sT_Box = tkinter.Entry(root, textvariable = sT_Input) #Text(root, height = 1, width = 10)

#nL = Label(text = "How many images do you want to find total: ")

#nL_Box = tkinter.Entry(root, textvariable = nL_Input) #Text(root, height = 1, width = 10)

#search = Button(root, text = "Search", command = takeInput)

#sT.pack()
#sT_Box.pack()
#nL.pack()
#nL_Box.pack()
#search.pack()

#exitButton = tkinter.Button(root, text = "Exit", command = close)
#exitButton.pack()

#root.mainloop()

searchTerm = input("What would you like images of in the dataset: ")
numLinks = input("How many images do you want to find total: ")
#searchTerm = sT_Input.get()
#numLinks = nL_Input.get()
totalNumLinks = int(numLinks)

#Leaving the parameter empty will make webdriver.Chrome() search for a default
#path to chromedriver.exe
#
#If you want to, you can specify the path like this:
#DRIVER_PATH = <YOUR PATH>
#wd = webdriver.Chrome(executable_path=DRIVER_PATH)

def getImageURLs(query:str, maxNumLinks:int, wd:webdriver, delay):
    def scrollToBottom(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    #Google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    #Loading the page
    wd.get(search_url.format(q=query))

    imageURLs = set()
    imageCount = 0
    resultsStart = 0
    
    while imageCount < maxNumLinks:
        scrollToBottom(wd)

        #Get image thumbnails
        thumbnailResults = wd.find_elements_by_css_selector("img.Q4LuWd")
        numResults = len(thumbnailResults)

        print(f"Found: {numResults} search results. Extracting links from {resultsStart}:{numResults}")

        for img in thumbnailResults[resultsStart:numResults]:
            #Try to click every thumbnail to get the real image
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            #Extract image URLs
            actualImages = wd.find_elements_by_css_selector('img.n3VNCb')
    
            for actualImage in actualImages:
                if (actualImage.get_attribute('src') and 'http' in actualImage.get_attribute('src')):
                    imageURLs.add(actualImage.get_attribute('src'))

            imageCount = len(imageURLs)

            #Found sufficient number of images so stop searching
            if (len(imageURLs) >= maxNumLinks):
                print(f"Found: {len(imageURLs)} image links, done!")
                break
            else:
                print("Found:", len(imageURLs), "image links, looking for more ...")
                time.sleep(5)
                #Possible bug here, no idea how to fix
                #continue
                loadMoreButton = wd.find_element(by = By.CSS_SELECTOR, value = ".mye4qd")
                if loadMoreButton:
                    wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        resultsStart = len(thumbnailResults)

    return imageURLs

def persistImages(folderPath:str, url:str):
    try:
        imageContent = requests.get(url).content
    except Exception as e:
        print(f"ERROR - Could not DOWNLOAD {url} - {e}")

    try:
        imageFile = io.BytesIO(imageContent)
        image = PIL.Image.open(imageFile).convert('RGB')
        filePath = os.path.join(folderPath, hashlib.sha1(imageContent).hexdigest()[:10] + '.jpg')
        with open(filePath, 'wb') as f:
            image.save(f, "JPEG", quality = 95)
        print(f"SUCCESS - saved {url} - as {filePath}")
    except Exception as e:
        print(f"ERROR - Could not SAVE {url} - {e}")

def searchAndDownload(search_term:str, targetPath, numImages:int):
    targetFolder = os.path.join(targetPath, '_'.join(search_term.lower().split(' ')))

    if (not os.path.exists(targetFolder)):
        os.makedirs(targetFolder)

    #Leaving the parameter empty will make webdriver.Chrome() search for a default
    #path to chromedriver.exe
    #
    #If you want to, you can specify the path like this:
    #DRIVER_PATH = <YOUR PATH>
    #wd = webdriver.Chrome(executable_path=DRIVER_PATH)
    with webdriver.Chrome() as wd:
        urls = getImageURLs(search_term, numImages, wd = wd, delay = 1)

    for elem in urls:
        persistImages(targetFolder, elem)

    wd.quit()
     
searchAndDownload(searchTerm, 'dataset', totalNumLinks)
