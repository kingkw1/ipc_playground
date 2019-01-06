import ipc
import time

# Variables
send_freq = 60 # message send frequency (hz)
nmssgs = send_freq*2

sleeptime = 1/send_freq
mssgcount = 0

sender = ipc.FTPSender()
generator = ipc.Generator()

print(sender.packer.size)
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
