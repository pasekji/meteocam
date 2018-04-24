import sys
import smbus
import time
import subprocess

bus = smbus.SMBus(1)

bus.write_byte_data(0x60, 0x26, 0xB9)

bus.write_byte_data(0x60, 0x13, 0x07)

bus.write_byte_data(0x60, 0x26, 0xB9)
time.sleep(1)	
data = bus.read_i2c_block_data(0x60, 0x00, 6)

tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
temp = ((data[4] * 256) + (data[5] & 0xF0)) / 16
altitude = tHeight / 16.0
cTemp = temp / 16.0
print cTemp

if cTemp > 128:
    cTemp = 256 - cTemp
    cTemp = -cTemp

print cTemp
fTemp = cTemp * 1.8 + 32

bus.write_byte_data(0x60, 0x26, 0x39)

bus.write_byte(0x40, 0xF5)
time.sleep(1)
data = bus.read_i2c_block_data(0x60, 0x00, 4)
data0 = bus.read_byte(0x40)
data1 = bus.read_byte(0x40)
pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
pressure = (pres / 4.0) / 1000.0
humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
print "Pressure : %.2f kPa" %pressure
print "Altitude : %.2f m" %altitude
print "Temperature in Celsius  : %.2f C" %cTemp
print "Temperature in Fahrenheit  : %.2f F" %fTemp
print "Relative Humidity is : %.2f %%" %humidity
pressure="%.2f" %pressure
altitude="%.2f" %altitude
cTemp="%.2f" %cTemp
fTemp="%.2f" %fTemp
print "starting upload..."
subprocess.Popen(['/home/pi/Desktop/MeteoCam/uploader', str(pressure), str(altitude), str(cTemp), str(fTemp), str(humidity)])
print "upload is done"
sys.exit(1)
