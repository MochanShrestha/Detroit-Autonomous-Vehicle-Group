import ffmpy
import subprocess
import errno
import threading
import numpy
import nclib

width = 1920
height = 1080

def generate_frames_ffmpynclib(a, v, done_decoding):
    # Setup the ffmpy library to decode frames
    ff = ffmpy.FFmpeg(inputs={'pipe:0': '-f h264'}, outputs={'pipe:1': '-f rawvideo -pix_fmt rgb24'})

    # Run the ffmpeg as a subprocess and hook up the input and output pipes
    try:
        ff.process = subprocess.Popen(
            ff._cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=None
        )
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise ffmpy.FFExecutableNotFoundError("Executable '{0}' not found".format(ff.executable))
        else:
            raise

    # Start the thread to write data that we get from the network to ffmpeg
    def write_data():
        nc = nclib.Netcat(listen=('', 2222))

        nwritten = 0
        while (1):
            #print("Getting some data")
            fdata = nc.recv()
            #print("Trying to write some data")
            if len(fdata) == 0:
                # print("Finished writing file")
                ff.process.stdin.close()
                break;
            ff.process.stdin.write(fdata)
            # ff.process.stdin.flush()
            nwritten = nwritten + len(fdata)
            #print("Wrote: " + str(nwritten))

    # Function to read the data from ffmpeg and copy it to shared memory
    def read_data():
        while (1):
            #print("Trying to read some data")
            raw_image = ff.process.stdout.read(width * height * 3)
            #print("Read some data")
            if len(raw_image) == 0:
                done_decoding.value = 1
                break
            image = numpy.fromstring(raw_image, dtype='uint8')
            frame = image.reshape((height, width, 3))

            memoryview(a).cast('B')[:] = frame.flatten()

            # Increment a frame number
            v.value = v.value + 1

            #print("Decoding frame " + str(v.value))

    # Start the reading and writing
    #threading._start_new_thread(write_data, ())
    threading._start_new_thread(read_data, ())
    #read_data()
    write_data()