
import nclib

nc = nclib.Netcat(listen=('', 2222))

f = open("nctest.h264", 'wb')
while(1):
    fdata = nc.recv()
    if len(fdata) == 0:
        break
    f.write(fdata)