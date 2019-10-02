print("pi-ring init")
#import pygame
import time
import os
import sys
import usb.core
import usb.util
import pyaudio
import wave
print("import done")
#os.putenv('SDL_AUDIODEV', '/dev/snd')
chunk = 44100
#pygame.init()
print("pygame inited")
f = wave.open("/home/pi/pi-ring/music.wav", "rb")
p = pyaudio.PyAudio()
print("music loaded")
stream = p.open(format = p.get_format_from_width(2),  
                channels = 1,  
                rate = 44100,  
                output = True)
#dev = usb.core.find(find_all=True)
#print([dev1 for dev1 in dev])

dev = usb.core.find(idVendor=0x258a)
#print(dev)

interface = 0
endpoint = dev[0][(0,0)][0]
#print(endpoint)
if dev.is_kernel_driver_active(interface) is True:
	dev.detach_kernel_driver(interface)
usb.util.claim_interface(dev, interface)

while True:
	try:
		data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
		if data[0] in [1, 2]:
			#read data  
			data = f.readframes(chunk)  

			#play stream  
			while data:  
				stream.write(data)  
				data = f.readframes(chunk)  
	except usb.core.USBError as e:
		print(e)

time.sleep(5)
