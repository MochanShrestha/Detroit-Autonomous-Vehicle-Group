
import cv2
import os

# Read each frame and then write out the frame as jpeg
def extractFrames(video_file):
    # Get the name of the file that we will be making
    prefix_path, file_ext = os.path.splitext(video_file)

    vid = cv2.VideoCapture(video_file)
    frame_count = 1
    while True:
        # Read the frame
        ret, frame = vid.read()
        if (ret == False):
            break

        # Output the image to a jpeg
        imgfilename = prefix_path + str(frame_count).zfill(5) + ".jpg"
        print ("Writing fraome " + str(frame_count) + " to file " + imgfilename)
        cv2.imwrite(imgfilename, frame)

        # Increment the frame count for the next iteration
        frame_count = frame_count + 1

# This is the video file we want to read in
VIDEO_FILE = './video/stopsigns.mp4'
extractFrames(VIDEO_FILE)