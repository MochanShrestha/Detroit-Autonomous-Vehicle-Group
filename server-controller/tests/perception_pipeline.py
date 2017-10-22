
import matplotlib.pyplot as plt
import cv2
import glob
import numpy as np
#from skimage import io

def filter_red(img):
    r_channel = img[:,:,0]
    g_channel = img[:,:,1]
    b_channel = img[:,:,2]
    rgbbinary = np.zeros_like(r_channel)

    rgbbinary[(r_channel >= 85) & (g_channel <= 48 ) & (b_channel <= 64 )] = 255

    return rgbbinary

def filter_red_rgbimage(img):
    # Get the channel of red values
    rchan = filter_red(img)

    # Make the rgb image for open_cv
    imgo = np.zeros_like(img)
    imgo[:,:,0] = rchan

    return imgo

def filter_red_box(img):
    rchan = filter_red(img)
    pts = cv2.findNonZero(rchan);
    return cv2.boundingRect(pts)

# Find all the
#def get_traffic_signs(img):
