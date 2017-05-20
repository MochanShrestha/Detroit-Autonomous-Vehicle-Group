__author__ = 'zhengwang'

import threading
import numpy as np
import cv2
import socket
import time

class VideoStreamingTest(object):

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    def __init__(self):
        # Set up the camera server
        self.server_socket = socket.socket()
        self.ip_address = self.get_ip_address()
        print("Binding to IP: {}:{}".format(self.ip_address, 8000))
        self.server_socket.bind((self.ip_address, 8000))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.connection = self.connection.makefile('rb')

        # Setup the ultra-sonic server
        self.server_socket2 = socket.socket()
        print("Binding to IP: {}:{}".format(self.ip_address, 8002))
        self.server_socket2.bind((self.ip_address, 8002))
        self.server_socket2.listen(0)
        self.connection2, self.client_address2 = self.server_socket2.accept()

        threading._start_new_thread(self.streaming_ultrasonic, ())
        self.streaming()

    def streaming(self):
        i = 0;
        try:
            print ("Connection from: ", self.client_address)
            print ("Streaming...")
            print ("Press 'q' to exit")

            stream_bytes = b""
            while True:
                myerror = self.connection.read(1024)
                # stream_bytes.append(int(myerror, 8))
                stream_bytes += myerror
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')

                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    # image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_GRAYSCALE)
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                    # try:
                    cv2.imshow('image', image)
                    #except:
                    #cv2.imwrite('im'+str(i)+".jpg", image)
                    #i+=1
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    #time.sleep(0.01)

                #break
        finally:
            self.connection.close()
            self.server_socket.close()

    def streaming_ultrasonic(self):

        try:
            print("Connection from: ", self.client_address2)
            start = time.time()

            while True:
                sensor_data = float(self.connection2.recv(1024))
                print("Distance: %0.1f cm" % sensor_data)

                # testing for 10 seconds
                if time.time() - start > 1000:
                    break
        finally:
            self.connection2.close()
            self.server_socket2.close()


if __name__ == '__main__':
    VideoStreamingTest()
