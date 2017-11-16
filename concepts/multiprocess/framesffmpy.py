
import ffmpy
import subprocess
import errno
import threading
import numpy

def generate_frames_ffmpy(a,v, done_decoding):
    # Setup the ffmpy library to decode frames
    ff = ffmpy.FFmpeg(inputs={'pipe:0': '-f h264'}, outputs={'pipe:1': '-f rawvideo -pix_fmt rgb24'})

    try:
        ff.process = subprocess.Popen(
            ff._cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise ffmpy.FFExecutableNotFoundError("Executable '{0}' not found".format(ff.executable))
        else:
            raise

    samplefile = open('sample.h264', 'rb')

    def write_data():
        while (1):
            print("Trying to write some data")
            fdata = samplefile.read(1920 * 1080)
            if len(fdata) == 0:
                print("Finished writing file")
                ff.process.stdin.close()
                break;
            ff.process.stdin.write(fdata)
            print("Wrote some data")

    threading._start_new_thread(write_data, ())

    while(1):
        print("Trying to read some data")
        raw_image = ff.process.stdout.read(1920 * 1080 * 3)
        print("Read some data")
        if len(raw_image) == 0:
            done_decoding.value = 1
            break
        image = numpy.fromstring(raw_image, dtype='uint8')
        frame = image.reshape((1080,1920,3))

        memoryview(a).cast('B')[:] = frame.flatten()

        # Increment a frame number
        v.value = v.value + 1

        print ("Decoding frame " + str(v.value))