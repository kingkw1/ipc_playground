import ftp
import time
from multiprocessing import Process
import sys

def send_ftp(send_freq = 60, dur = 2):
    # Initializations
    sleeptime = 1/send_freq
    mssgcount = 0
    nmssgs = send_freq*dur
    sender = ftp.FTPSender()
    generator = ftp.Generator()

    try:
        while mssgcount < nmssgs:
            data = generator.generate_data_message()
            sender.send(data)
            mssgcount += 1
            time.sleep(sleeptime)
    except KeyboardInterrupt:
        pass

    sender.send(generator.generate_stop_message())
    sender.close()

    print("Messages sent:  ", mssgcount)

def recv_ftp(fname='test_ftp.csv'):
    receiver = ftp.FTPReceiver()
    writer = ftp.Stenographer(fname)

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

if __name__ == "__main__":
    sender = Process(target=send_ftp)
    receiver = Process(target=recv_ftp)

    receiver.start()
    time.sleep(0.01)
    sender.start()

    receiver.join()
    sender.join()

    if receiver.exitcode == 0 & sender.exitcode == 0:
        print("test_ftp run complete! No errors!")
    else:
        raise NotImplementedError()
