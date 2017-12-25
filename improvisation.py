#! /usr/bin/env python

# uses some code from http://www.pyimagesearch.com/2015/05/04/target-acquired-finding-targets-in-drone-and-quadcopter-video-streams-using-python-and-opencv/

import numpy as np
import time
import argparse
import cv2
import grid
import math
import socket
import random

CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4

GRID_COLOR = (34,139,45)
TEXT_COLOR =CHORD_COLOR = (100,255,255)
TARGET_COLOR = (50,50,200)
#TEXT_COLOR = (120,120,120)
GRID_STROKE_WIDTH = 2
TARGET_STROKE_WIDTH = 2
INTERVAL = 0.2

PD_IP = "127.0.0.1"
PD_PORT = 3000

cap = cv2.VideoCapture(1)
cap.set(CV_CAP_PROP_FRAME_WIDTH,1280);
cap.set(CV_CAP_PROP_FRAME_HEIGHT,720);

last_change = time.time()
current_x = 640
current_y = 360

current_chord = [0,0,0]

current_freqs = {}
previous_freqs = {}

# inititalize
for x in range (60,72):
    current_freqs[x] = 0;
    previous_freqs[x] = 0;

ap = argparse.ArgumentParser()
ap.add_argument("-g", "--gamma", 
    required=False, 
    default='1', 
    help="Gamma correction value (default = 1)")
args = vars(ap.parse_args())
mygamma = float(args["gamma"])

# create a socket for communicating with pd          
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
sock.connect((PD_IP, PD_PORT))


def adjust_gamma(image, gamma=1.0):
    # apply gamma correction using the lookup table
    return cv2.LUT(image, getTable(gamma))

def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:        
            memo[x] = f(x)
        return memo[x]
    return helper


@memoize
def getTable(gamma):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    return table


def distToFreq(dist):
    return (-0.8*dist) + 300

def calculateDistance(node):
    return (node[0], math.sqrt(math.pow(current_x-node[1][0],2) + math.pow(current_y-node[1][1],2)))

def playChord():
    # calculate the distances and order by distance
    distances = sorted(map(calculateDistance, grid.nodes), key=lambda tup: tup[1])
    # update current_chord
    for x in range (0,3):
        current_chord[x] = distances[x][0]
    current_chord.sort()
    # update current_freqs
    for distance in distances:
        current_freqs[distance[0]] = distToFreq(distance[1]) if distance[0] in current_chord else 0 
    # send new frequeny if different
    for x in range (60,72):
        if current_freqs[x] != previous_freqs[x]:
            sock.send(str(x) + " " + str(current_freqs[x]) + ";")
            previous_freqs[x] = current_freqs[x]

def drawGrid(frame):
    # draw edges
    for edge in grid.edges:
        edge_color = CHORD_COLOR if grid.nodes[edge[0]][0] in current_chord and grid.nodes[edge[1]][0] in current_chord else GRID_COLOR
        cv2.line(frame,grid.nodes[edge[0]][1],grid.nodes[edge[1]][1],edge_color,GRID_STROKE_WIDTH,cv2.CV_AA)
    # draw nodes
    for node in grid.nodes:
        node_color = CHORD_COLOR if node[0] in current_chord else GRID_COLOR
        cv2.circle(frame, node[1],16,node_color,-1, cv2.CV_AA)
        text_offset = 10 if len(node[2]) == 2 else 6    
        cv2.putText(frame, str(node[2]), (node[1][0]-text_offset,node[1][1]+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0), 1)



# main loop
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = adjust_gamma(frame, mygamma)
    status = "no target" 
    # grab the current frame and initialize the status text
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(blurred, 50, 150)
	# find contours in the edge map
    (contours, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   
    drawGrid(frame)
    # loop over the contours
    for contour in contours:
        # approximate the contour
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * peri, True)

        # ensure that the approximated contour is "roughly" rectangular
        if len(approx) >= 4 and len(approx) <= 6:
            # compute the bounding box of the approximated contour and
            # use the bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            aspectRatio = w / float(h)
            # compute the solidity of the original contour
            area = cv2.contourArea(contour)
            hullArea = cv2.contourArea(cv2.convexHull(contour))
            solidity = area / float(hullArea)

            # compute whether or not the width and height, solidity, and
            # aspect ratio of the contour falls within appropriate bounds
            keepDims = w > 25 and h > 25
            keepSolidity = solidity > 0.7
            keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2

            # ensure that the contour passes all our tests
            if keepDims and keepSolidity and keepAspectRatio:
                # draw an outline around the target 
                # cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
                # compute the center of the contour region and draw crosshairs
                M = cv2.moments(approx)
                (cX, cY) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                #status = "x: " + str(cX) +   "y: " + str(cY)
                (startX, endX) = (int(cX - 15), int(cX + 15))
                (startY, endY) = (int(cY - 15), int(cY + 15))
                cv2.line(frame, (startX, cY), (endX, cY), TARGET_COLOR, TARGET_STROKE_WIDTH)
                cv2.line(frame, (cX, startY), (cX, endY), TARGET_COLOR, TARGET_STROKE_WIDTH)
                # every INTERVAL seconds calculate new chord
                if time.time() - last_change > INTERVAL:
                    last_change = time.time()
                    current_x = cX
                    current_y = cY
                    playChord()

    # draw current position
    cv2.circle(frame, (current_x,current_y),25,TARGET_COLOR,TARGET_STROKE_WIDTH),
    # draw the status text on the frame
    key = ','.join(str(e) for e in current_chord)
    str_chord = ""
    if key in grid.chords:
        str_chord = " chord: " + grid.chords[key]
    status = "x: " + str(current_x) + " y: " + str(current_y) + str_chord
    cv2.putText(frame, status, (22, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, TEXT_COLOR, 2)
    # Display the resulting frame
    cv2.imshow('improvisation',frame)
    # cv2.imshow('edged',edged)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


for x in range (60,72):
    sock.send(str(x) + " 0.0000" + str(random.randint(1,99)) +";")
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
