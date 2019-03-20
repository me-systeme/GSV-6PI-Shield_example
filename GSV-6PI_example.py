import serial
import struct
import RPi.GPIO as GPIO
from time import strftime, sleep
 
def f_MesswertEmpfangen():
	tupel_messwerte = ("leer",)
	flag = False
	praefix = verbindung.readline(1)
	praefix = praefix.encode("hex")
	if praefix == "aa":
		identifier = verbindung.readline(1)
		identifier = identifier.encode("hex")
		if identifier == "15":
			rest = verbindung.readline(26)
			rest = rest.encode("hex")
			Antwort = praefix + identifier + rest
			if len(Antwort) == 56:
				ch1 = byte_to_value(Antwort[6:14], "float")
				ch2 = byte_to_value(Antwort[14:22], "float")
				ch3 = byte_to_value(Antwort[22:30], "float")
				ch4 = byte_to_value(Antwort[30:38], "float")
				ch5 = byte_to_value(Antwort[38:46], "float")
				ch6 = byte_to_value(Antwort[46:54], "float")
				tupel_messwerte = ((strftime("%Y.%m.%d %H:%M:%S"),ch1,ch2,ch3,ch4,ch5,ch6),)
				flag = True
	return flag, tupel_messwerte		# return: Messwert-Tupel und bool, ob Messwert empfangen wurde
 
def antwort_empfangen(verbindung):
	var_routine = True
	while (var_routine == True) :
		praefix = verbindung.readline(1)								# lese praefix
		praefix = praefix.encode("hex")									# string to hexstring
		if praefix == "aa":
			identifier = verbindung.readline(1)							# lese identifier
			identifier = identifier.encode("hex")						# identifier: string to hexstring
			if (identifier != 0x15):									# Identifier vergleichen
				rest = verbindung.readline(int(identifier)-0x50+2)		# lese Rest des strings
				rest = rest.encode("hex")								# Rest: string to hexstring
				Antwort = praefix + identifier + rest					# string zusammensetzen
				print "Antwort: " + Antwort								# print Antwortframe
				var_routine = False
	return Antwort
 
def byte_to_value(daten, typ):
	if (typ == "u8") or (typ == "i8"):			# uint 8 Byte
		Multiplikator = [16,1]
	if (typ == "u16") or (typ == "i16"):		# uint 16 Byte
		Multiplikator = [4096,256,16,1]
	if (typ == "u32") or (typ == "i32"):		# uint 32 Byte
		Multiplikator = [268435456,16777216,1048576,65536,4096,256,16,1]
	if typ == "float":							# uint 32 Byte
		Multiplikator = [268435456,16777216,1048576,65536,4096,256,16,1]
	MW_list = []
	for i in range(len(Multiplikator)):
		MW_list.append(int(daten[i:(i+1)], 16))
	MW = 0
	for k in range(len(Multiplikator)):
		MW += ( MW_list[k] * Multiplikator[k] )
	if typ == "float":
		MW = struct.pack("I", MW)
		MW = struct.unpack("f", MW)[0]
	if (typ == "i8"):
		MW = MW - 16
	if (typ == "i16"):
		MW = MW - 4096
	if (typ == "i32"):
		MW = MW - 268435456
	return MW
 
def value_to_byte(MW, typ):
	if (typ == "u8") or (typ == "i8"):			# uint 8 Byte
		MW = int(MW)
		Teiler = [16,1]
	if (typ == "u16") or (typ == "i16"):		# uint 16 Byte
		MW = int(MW)
		Teiler = [4096,256,16,1]
	if (typ == "u32") or (typ == "i32"):		# uint 32 Byte
		MW = int(MW)
		Teiler = [268435456,16777216,1048576,65536,4096,256,16,1]
	if typ == "float":							# float
		print ("MW: ",MW)
		MW = struct.pack("f", float(MW))
		MW = struct.unpack("I", MW)
		print MW[0]
		print MW
		MW = MW[0]
		Teiler = [268435456,16777216,1048576,65536,4096,256,16,1]
	if (typ == "i8"):
		MW = MW + 16
	if (typ == "i16"):
		MW = MW + 4096
	if (typ == "i32"):
		MW = MW + 268435456
	list_MW=[]
	for i in range(len(Teiler)):
		list_MW.append(MW / Teiler[i])
		MW = MW % Teiler[i]
	for i in range(len(list_MW)):
		list_MW[i] = hex(list_MW[i])						# in hex-str umwandeln
		list_MW[i] = list_MW[i][2:]							# "0x" entfernen
	list_bytes = []
	for i in range(len(list_MW)/2):
		list_bytes.append(list_MW[i*2] + list_MW[(i*2)+1])	# Zeichen paarweise buendeln und in neues array schreiben
	for i in range(len(list_bytes)):
		list_bytes[i] = int(list_bytes[i],16)				# str to hex_int
	str_bytes = ""											# dummy fuer Datenstring
	for i in range(len(list_bytes)):
		str_bytes += chr(list_bytes[i])						# datenstring erstellen
	return str_bytes										# Datenstring zurueckgeben
 
if __name__ == '__main__':
	GPIO.setmode(GPIO.BCM)									# Pin fuer GSV-6_Einschalten
	GPIO.setup(12,GPIO.OUT)
	GPIO.output(12,1)										# GSV-6 einschalten
	verbindung = serial.Serial('/dev/ttyAMA0', 230400, timeout=1)
	verbindung.isOpen()
 
	verbindung.write(chr(0xAA)+chr(0x90)+chr(0x23)+chr(0x85))	# stop transmission
	sleep(0.5)
	Antwort = antwort_empfangen(verbindung)
	verbindung.write(chr(0xAA)+chr(0x90)+chr(0x1f)+chr(0x85))	# get SerNo
	print("Seriennummer: ",byte_to_value(antwort_empfangen(verbindung)[6:-1],'u32'))
	sleep(0.5)
	verbindung.write(chr(0xAA)+chr(0x90)+chr(0x24)+chr(0x85))	# start transmission
	
	x = raw_input("Antwortframes [A/a] / Messwerte [M/m] / permanent [P/p]")
	try:
		while True:
			if x in ["a","A"]:
				praefix = verbindung.readline(1)			# lese praefix
				praefix = praefix.encode("hex")				# string to hexstring
				if praefix == "aa":
					rest = verbindung.readline(27)			# lese rest
					rest = rest.encode("hex")				# rest: string to hexstring
					Antwort = praefix + rest				# string zusammensetzen
					print("Antwort: {0:s}".format(Antwort))	# print Antwortframe
			if x in ["p","P"]:
				while True:
					praefix = verbindung.readline(30)
					praefix = praefix.encode("hex")	
					print praefix							# print Antwortframe
			if x in ["m","M"]:
				flag_f = False
				flag_f, tupel_MWe_f = f_MesswertEmpfangen()
				if flag_f == True:							# wenn ein Messwert empfangen wurde...
					for i in range(6):
						print("Kanal {0:1d}: {1:5.6f}".format((i+1),tupel_MWe_f[0][i+1]))
			print "-"*20
 
	except KeyboardInterrupt:
		pass
	
	verbindung.close()	# serielle Verbindung schliessen
	GPIO.output(12,0)	# GSV-6 ausschalten
	GPIO.cleanup()
	
	print "\nProgrammende"
