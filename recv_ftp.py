import ipc

receiver = ipc.FTPReceiver()
writer = ipc.Stenographer('test_ftp.csv')

mssgcount = 0
try:
    while True:
        data = receiver.recv()
        if data[0] == 0:
            break
        else:
            writer.write(data)
            mssgcount += 1
except KeyboardInterrupt:
    pass

receiver.close()
print("Messages recieved:  ", mssgcount)
