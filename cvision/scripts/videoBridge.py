#!/usr/bin/env python

import rospy
import numpy as np
import cv2
import imutils
import math
import time

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

# Check version of OpenCV

if cv2.__version__.startswith('2'):
    OLDCV = True
else:
    OLDCV = False
    
if OLDCV:
    import cv2.cv as cv

# Import vision parameters

import cvisionParams


###################################

def videoBridge():

    # initialize node
    rospy.init_node('videoBridge', anonymous=True)

    # get namespace
    ns = rospy.get_namespace()
    ns = ns[0:len(ns)-1]

    cvisionParams.setParams(ns)
    
    # Create publishers

    frame = rospy.Publisher(ns+'/cvision/frame', Image, queue_size=10)
    msg = CvBridge()

    # set publication rate
    rate = rospy.Rate(rospy.get_param(ns+'/cvision/loopRate'))
    
    # start video stream and set parameters
    cap = cv2.VideoCapture(0)
    if OLDCV:
        cap.set(cv.CV_CAP_PROP_FPS, rospy.get_param(ns+'/cvision/loopRate'))
        cap.set(cv.CV_CAP_PROP_FRAME_WIDTH, rospy.get_param(ns+'/cvision/LX'))
        cap.set(cv.CV_CAP_PROP_FRAME_HEIGHT, rospy.get_param(ns+'/cvision/LY'))
    else:
        cap.set(cv2.CAP_PROP_FPS, rospy.get_param(ns+'/cvision/loopRate'))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, rospy.get_param(ns+'/cvision/LX'))
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, rospy.get_param(ns+'/cvision/LY'))
     
    # wait a second
    time.sleep(1.0)
    
    if cap.isOpened():
        print 'videoBridge initialized...'
    else:
        print 'videoBridge error...'
        
    while not rospy.is_shutdown():

        # grab a frame
        _, bgr = cap.read()
        
        # resize if needed
        # if rospy.get_param('/cvision/reduce'):
        #     bgr = cv2.resize(bgr,(rospy.get_param('/cvision/LX'),rospy.get_param('/cvision/LY')))
        
        # convert to grayscale
        
        # gry = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

        # publish images
        rate.sleep()
        frame.publish(msg.cv2_to_imgmsg(bgr, encoding="bgr8"))

if __name__ == '__main__':
    try:
        videoBridge()
    except rospy.ROSInterruptException:
        # cleanup the camera and close any open windows
        #cap.release()
        cv2.destroyAllWindows()
pass
