
import cv2
import time

def generate_frames(a,v, done_decoding):
    # Load video files and start producing the frames
    vid = cv2.VideoCapture('sample.h264')

    # Loop until we reach the end of the file
    while True:
        start = time.time()
        # Get the frame data
        ret, frame = vid.read()
        end = time.time()
        print("Read frame: " + str(end-start))

        # Check if we are done with the data
        if (ret == False):
            done_decoding.value = 1
            break

        start = time.time()
        # Copy over the data to the shared memory
        memoryview(a).cast('B')[:] = frame.flatten()
        end = time.time()
        print("Copy frame: " + str(end-start))

        # Increment a frame number
        v.value = v.value + 1

        print ("Decoding frame " + str(v.value))