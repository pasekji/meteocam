#!/usr/bin/env python
# !!! TENTO SCRIPT JIŽ NENÍ V KASKÁDĚ POUŽIT A JE ZDE POUZE JAKO PŘÍKLAD PROVEDENÍ V JAZYCE PYTHON, NAHRADIL HO NOVĚJŠÍ SCRIPT cam-get.sh !!! 
# Nejprve provádíme import několika knihoven těmito příkazy: 
from time import sleep	
import picamera
import datetime
import time
timeNow = datetime.datetime.now()	# Do této proměnné ukládáme nynější datum a čas. 
camera = picamera.PiCamera()		# Tímto příkazem definujeme kameru. 
camera.resolution = (1920, 1080)	# Tímto příkazem si navolíme rozlišení kamery. Výchozí rozlišení je Full HD. 
time.sleep(1)						# Kamera se musí před snímkem nejprve trochu zorientovat, proto jí dáme tímto příkazem sekundovou pauzu. 
camera.capture("/media/pi/73EA-9457/Pictures/Pictures-unstamped/" + time.strftime("%y%m%d_%H-%M-%S") + ".jpg")	# Tímto příkazem již pořizujeme snímek přímo z kamery, který se ukládá do zvoleného adresáře s názevm časové značky.
print ("New picture has been taken!")