#! /usr/bin/env python

# based on code from http://www.pyimagesearch.com/2015/05/04/target-acquired-finding-targets-in-drone-and-quadcopter-video-streams-using-python-and-opencv/
import numpy as np
import time
import cv2
import grid

CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4

GRID_COLOR = (34,139,45)
TARGET_COLOR = (50,50,200)
GRID_STROKE_WIDTH = 2
INTERVAL = 0.5

cap = cv2.VideoCapture(2)
cap.set(CV_CAP_PROP_FRAME_WIDTH,1280);
cap.set(CV_CAP_PROP_FRAME_HEIGHT,720);

last_change = time.time()
current_x = 640
current_y = 360

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    status = "no target" 

    # grab the current frame and initialize the status text
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(blurred, 50, 150)

	# find contours in the edge map
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # draw the grid
    for edge in grid.edges:
        cv2.line(frame,grid.nodes[edge[0]][1],grid.nodes[edge[1]][1],GRID_COLOR,GRID_STROKE_WIDTH,cv2.CV_AA)

    for node in grid.nodes:
        cv2.circle(frame, node[1],14,GRID_COLOR,-1, cv2.CV_AA),
        cv2.putText(frame, str(node[2]), (node[1][0]-10,node[1][1]+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0), 1)

    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)

        # ensure that the approximated contour is "roughly" rectangular
        if len(approx) >= 4 and len(approx) <= 6:
            # compute the bounding box of the approximated contour and
            # use the bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            aspectRatio = w / float(h)

            # compute the solidity of the original contour
            area = cv2.contourArea(c)
            hullArea = cv2.contourArea(cv2.convexHull(c))
            solidity = area / float(hullArea)

            # compute whether or not the width and height, solidity, and
            # aspect ratio of the contour falls within appropriate bounds
            keepDims = w > 25 and h > 25
            keepSolidity = solidity > 0.9
            keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2

            # ensure that the contour passes all our tests
            if keepDims and keepSolidity and keepAspectRatio:
                # draw an outline around the target and update the status
                # text
                #cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
                

                # compute the center of the contour region and draw the
                # crosshairs
                M = cv2.moments(approx)
                (cX, cY) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                #status = "x: " + str(cX) +   "y: " + str(cY)

                (startX, endX) = (int(cX - 15), int(cX + 15))
                (startY, endY) = (int(cY - 15), int(cY + 15))
                cv2.line(frame, (startX, cY), (endX, cY), TARGET_COLOR, 2)
                cv2.line(frame, (cX, startY), (cX, endY), TARGET_COLOR, 2)

                # every INTERVAL seconds calculate new chord
                if time.time() - last_change > INTERVAL:
                    last_change = time.time()
                    current_x = cX
                    current_y = cY

    # draw current position
    cv2.circle(frame, (current_x,current_y),14,TARGET_COLOR,2),

    # draw the status text on the frame
    status = "x: " + str(current_x) + " y: " + str(current_y)
    cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_PLAIN, 1,TARGET_COLOR, 2)


    # Display the resulting frame
    cv2.imshow('carplusplus',frame)
    ##cv2.imshow('frame2',edged)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
