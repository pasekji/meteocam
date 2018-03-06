# MPL3115A2 a SI7021_I2CS
# Tento kód je navržen pro práci s MPL3115A2_I2CS I2C Mini modulem a SI7021_I2CS modulem dostupných na ControlEverything.com.
# https://www.controleverything.com/products

# Import potřebných knihoven 
import sys
import smbus
import time
import subprocess

# V následující proměnné si zvolíme počáteční id v databázové tabulce. Je možné jej definovat přímo, nebo prvním argumentem při spuštění.  
idStats = int(sys.argv[1])
idAverage = int(sys.argv[2])
frequency = int(sys.argv[3])					 
count = 1						# Tato proměnná vyjadřuje počet průchodů. Jeden za 10 minut > 144 denně.

# Nekončící cyklus, podmínka True je splněna vždy.
while True:
# Podmínka pro ověření počtu průchodů. 
    if count <= 144:
	
		# MPL3115A2 adresa, 0x60(96)
		# Zvolení ovládacího registru, 0x26(38)
		# 0xB9(185)	Aktivní mód, OSR = 128, Mód výškoměru
        bus.write_byte_data(0x60, 0x26, 0xB9)
	
		# MPL3115A2 adresa, 0x60(96)
		# Zvolení registru pro ovládání dat, 0x13(19)
		# 0x07(07) Data připravena a povolena pro nadmořskou výšku, atmosférický tlak, teplotu.
        bus.write_byte_data(0x60, 0x13, 0x07)
	
		# MPL3115A2 adresa, 0x60(96)
		# Zvolení ovládacího registru, 0x26(38)
		# 0xB9(185) Aktivní mód, OSR = 128, Mód výškoměru
        bus.write_byte_data(0x60, 0x26, 0xB9)

		# Pauza pro ustálení konfigurace
        time.sleep(1)	

		# MPL3115A2 adresa, 0x60(96)
		# Čti data z 0x00(00), 6 bytů
		# status, tHeight MSB1, tHeight MSB, tHeight LSB, temp MSB, temp LSB
        data = bus.read_i2c_block_data(0x60, 0x00, 6)

		# Převod dat do 20-bitů		
        tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
        temp = ((data[4] * 256) + (data[5] & 0xF0)) / 16
        altitude = tHeight / 16.0
        cTemp = temp / 16.0
        print cTemp
	
		# Fukce pro převod negativních hodnot
        if cTemp > 128:
            cTemp = 256 - cTemp
            cTemp = -cTemp
        
        print cTemp
        fTemp = cTemp * 1.8 + 32
	
		# MPL3115A2 adresa, 0x60(96)
		# Zvolení ovládacího registru, 0x26(38)
		# 0x39(57) Aktivní mód, OSR = 128, Mód tlakoměru
        bus.write_byte_data(0x60, 0x26, 0x39)

		# SI7021 address, 0x40(64)
		# 0xF5(245) Zvolení módu Relativní vlhkosti
        bus.write_byte(0x40, 0xF5)

		# Pauza pro ustálení konfigurace
        time.sleep(1)

		# MPL3115A2 adresa, 0x60(96)
		# Čti data z 0x00(00), 4 byty
		# status, pres MSB1, pres MSB, pres LSB
        data = bus.read_i2c_block_data(0x60, 0x00, 4)
	
		# SI7021 adresa, 0x40(64)
		# Čti data, 2 byty, nejdříve vlhkost MSB
        data0 = bus.read_byte(0x40)
        data1 = bus.read_byte(0x40)
	
		# Převod dat do 20-bitů
        pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
        pressure = (pres / 4.0) / 1000.0
        humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6

		# Výpis získaných dat na obrazovku
        print "Pressure : %.2f kPa" %pressure
        print "Altitude : %.2f m" %altitude
        print "Temperature in Celsius  : %.2f C" %cTemp
        print "Temperature in Fahrenheit  : %.2f F" %fTemp
        print "Relative Humidity is : %.2f %%" %humidity
        pressure="%.2f" %pressure
        altitude="%.2f" %altitude
        cTemp="%.2f" %cTemp
        fTemp="%.2f" %fTemp

		# Spuštení subprocesu pro zavedení průměrných hodnot do dazabáze na serveru 		
        subprocess.Popen(['/home/pi/Desktop/MeteoCam/avg-temp', str(idAverage)])
        idAverage +=1
		
        print "starting upload..."
 
		# Spuštení subprocesu pro upload dat do databáze na serveru 
        subprocess.Popen(['/home/pi/Desktop/MeteoCam/uploader', str(idStats), str(pressure), str(altitude), str(cTemp), str(fTemp), str(humidity)])
        print "upload is done"
        idStats +=1
        print count
        count +=1
        time.sleep(frequency)
    
    else:
		# Resetování hodnot
        count = 1
        avgTemp = 0
        avgHumid = 0
        
		# MPL3115A2 adresa, 0x60(96)
		# Zvolení ovládacího registru, 0x26(38)
		# 0xB9(185)	Aktivní mód, OSR = 128, Mód výškoměru
        bus.write_byte_data(0x60, 0x26, 0xB9)
	
		# MPL3115A2 adresa, 0x60(96)
		# Zvolení registru pro ovládání dat, 0x13(19)
		# 0x07(07) Data připravena a povolena pro nadmořskou výšku, atmosférický tlak, teplotu.
        bus.write_byte_data(0x60, 0x13, 0x07)
	
		# MPL3115A2 adresa, 0x60(96)
		# Zvolení ovládacího registru, 0x26(38)
		# 0xB9(185) Aktivní mód, OSR = 128, Mód výškoměru
        bus.write_byte_data(0x60, 0x26, 0xB9)

		# Pauza pro ustálení konfigurace
        time.sleep(1)	

		# MPL3115A2 adresa, 0x60(96)
		# Čti data z 0x00(00), 6 bytů
		# status, tHeight MSB1, tHeight MSB, tHeight LSB, temp MSB, temp LSB
        data = bus.read_i2c_block_data(0x60, 0x00, 6)

		# Převod dat do 20-bitů		
        tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
        temp = ((data[4] * 256) + (data[5] & 0xF0)) / 16
        altitude = tHeight / 16.0
        cTemp = temp / 16.0
        print cTemp
	
		# Fukce pro převod negativních hodnot
        if cTemp > 128:
            cTemp = 256 - cTemp
            cTemp = -cTemp
        
        print cTemp
        fTemp = cTemp * 1.8 + 32
	
		# MPL3115A2 adresa, 0x60(96)
		# Zvolení ovládacího registru, 0x26(38)
		# 0x39(57) Aktivní mód, OSR = 128, Mód tlakoměru
        bus.write_byte_data(0x60, 0x26, 0x39)

		# SI7021 address, 0x40(64)
		# 0xF5(245) Zvolení módu Relativní vlhkosti
        bus.write_byte(0x40, 0xF5)

		# Pauza pro ustálení konfigurace
        time.sleep(1)

		# MPL3115A2 adresa, 0x60(96)
		# Čti data z 0x00(00), 4 byty
		# status, pres MSB1, pres MSB, pres LSB
        data = bus.read_i2c_block_data(0x60, 0x00, 4)
	
		# SI7021 adresa, 0x40(64)
		# Čti data, 2 byty, nejdříve vlhkost MSB
        data0 = bus.read_byte(0x40)
        data1 = bus.read_byte(0x40)
	
		# Převod dat do 20-bitů
        pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
        pressure = (pres / 4.0) / 1000.0
        humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6

		# Výpis získaných dat na obrazovku
        print "Pressure : %.2f kPa" %pressure
        print "Altitude : %.2f m" %altitude
        print "Temperature in Celsius  : %.2f C" %cTemp
        print "Temperature in Fahrenheit  : %.2f F" %fTemp
        print "Relative Humidity is : %.2f %%" %humidity
        pressure="%.2f" %pressure
        altitude="%.2f" %altitude
        cTemp="%.2f" %cTemp
        fTemp="%.2f" %fTemp

		# Spuštení subprocesu pro zavedení průměrných hodnot do dazabáze na serveru 		
        subprocess.Popen(['/home/pi/Desktop/MeteoCam/avg-temp', str(idAverage)])
        idAverage +=1
		
        print "starting upload..."
 
		# Spuštení subprocesu pro upload dat do databáze na serveru 
        subprocess.Popen(['/home/pi/Desktop/MeteoCam/uploader', str(idStats), str(pressure), str(altitude), str(cTemp), str(fTemp), str(humidity)])
        print "upload is done"
        idStats +=1
        print count
        count +=1
        time.sleep(frequency)