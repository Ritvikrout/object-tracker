import cv2
import math
import time

p1 = 530
p2 = 300

xs = []
ys = []

video = cv2.VideoCapture('bb3.mp4')

#Load Tracker
tracker = cv2.TrackerCSRT_create()

#Read the first Frame of the Video
returned, img = video.read()

#Select The Bounding Box on the image
bbox = cv2.selectROI('tracking', img, False)

#Initialize the tracker on the image and the bounding box
tracker.init(img, bbox)
print(bbox)

def drawBox (img, bbox) :
    x,y,w,h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x,y), ((x+w),(y+h)), (255, 0, 255), 3, 1)
    cv2.putText(img,'Tracking', (75, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

def goal_track (img, bbox) :
    x,y,w,h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    #Get the centre point of the bounding box
    c1 = x+int(w/2)
    c2 = y+int(h/2)

    #Draw a small circle using centre points
    cv2.circle(img, (c1, c2), 2, (0, 0, 255), 5)
    cv2.circle(img, (int(p1), int(p2)), 2 ,(0, 255, 0), 3)

    #Calculate the distance 
    dist = math.sqrt(((c1 - p1)**2)+ ((c2- p2)**2))
    print(dist)

    #Goal is reached if distance is less than 20 distance points
    if (dist <= 20):
        cv2.putText(img,'Goal', (75, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    xs.append(c1)
    ys.append(c2)

    for i in range(len(xs)-1) :
        cv2.circle(img, (xs[i], ys[i]), 2, (0,0,255), 5)


while True :
    check, img = video.read()

    #Update the tracker on the image and the bounding box
    success, bbox = tracker.update(img)

    #Call DrawBox
    if success :
        drawBox(img, bbox)
    else :
        cv2.putText(img,'Lost', (75, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

    #Call Goal_track
    goal_track(img, bbox)

    cv2.imshow('video', img)

    key = cv2.waitKey(25)
    if key == 32 :
        print('Stopped')
        break

video.release()
