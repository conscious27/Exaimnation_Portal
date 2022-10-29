from telnetlib import LOGOUT
from urllib import response
from django.shortcuts import render, redirect
from django.contrib import messages
import threading
import cv2
import dlib

from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave
# import os

# test function for thread
def task1():
    # Connects to your computer's default camera
    cap = cv2.VideoCapture(0)
        
        
    # Detect the coordinates
    detector = dlib.get_frontal_face_detector()

    global cheating_detected
    cheating_detected = False
    # Capture frames continuouslyq
    while True:
        
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        
        # RGB to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        
        # Iterator to count faces
        global i
        i = 0
        for face in faces:
        
            # Get the coordinates of faces
            x, y = face.left(), face.top()
            x1, y1 = face.right(), face.bottom()
            cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
        
            # Increment iterator for each face in faces
            i = i+1

            if i>1:
                print("cheating detected")
                cheating_detected = True
        
            # Display the box and faces
            cv2.putText(frame, 'face num'+str(i), (x-10, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            print(face, i)
        
        # Display the resulting frame
    
        cv2.imshow('frame', frame)
        global stop_threads
        if stop_threads:
            break
    cap.release()
    cv2.destroyAllWindows()

# Create your views here.
def exampage(request):
    global stop_threads
    global i
    global cheating_detected
    stop_threads = False
    t1 = threading.Thread(target=task1, name="t1")
    t1.start()
    if request.method == "POST":
        answer1 = request.POST.get("a1")
        answer2 = request.POST.get("a2")
        answer3 = request.POST.get("a3")
        answer4 = request.POST.get("a4")
        answer5 = request.POST.get("a5")
        answer6 = request.POST.get("a6")
        answer7 = request.POST.get("a7")
        answer8 = request.POST.get("a8")
        answer9 = request.POST.get("a9")
        answer10 = request.POST.get("a10")

        count = 0

        if(answer1!=""):
            count +=1
        if(answer2!=""):
            count +=1
        if(answer3!=""):
            count +=1
        if(answer4!=""):
            count +=1
        if(answer5!=""):
            count +=1
        if(answer6!=""):
            count +=1
        if(answer7!=""):
            count +=1
        if(answer8!=""):
            count +=1
        if(answer9!=""):
            count +=1
        if(answer10!=""):
            count +=1

        if cheating_detected:
            print("hellp")
            message = "Cheating Detected!"
            messages.success(request, message)
            stop_threads= True
            t1.join()
            return redirect('completion')


        message = "total marks gained: " + str(count)
        messages.success(request, message)
        stop_threads= True
        t1.join()

        return redirect('completion')
    return render(request, 'takeexam/exampage.html')

def completion(request):
    return render(request, 'takeexam/completion.html')