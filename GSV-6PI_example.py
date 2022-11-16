import serial
import struct
import RPi.GPIO as GPIO
from time import strftime, sleep, time

class GSV6():
	def __init__(self):
		GPIO.setmode(GPIO.BCM)	  
		GPIO.setup(12,GPIO.OUT)
		GPIO.output(12,1) 
		self.verbindung = serial.Serial('/dev/ttyAMA0', 230400, timeout=0.1)
		self.verbindung.isOpen()

	def close(self):
		self.verbindung.close()	# serielle Verbindung schliessen
		GPIO.output(12,0)	# GSV-6 ausschalten
		GPIO.cleanup()

	def clearInputBuffer(self):
		sleep(0.1)
		self.verbindung.reset_input_buffer()

	def stopTransmission(self):
		self.verbindung.write(b'\xAA\x90\x23\x85')
		self.clearInputBuffer()
		


	def startTransmission(self):
		self.verbindung.write(b'\xAA\x90\x24\x85')
		self.clearInputBuffer()

	def resetGSV6(self):
		self.verbindung.write(b'\xAA\x90\x78\x85')
		sleep(1)

	def getDataRate(self):
		self.verbindung.write(b'\xAA\x90\x8A\x85')
		answ = self.verbindung.read(100)[3:7]
		self.clearInputBuffer()
		print(f"Datenrate: {struct.unpack('>f', answ)[0]}")

	def getSerNo(self):
		self.verbindung.write(b'\xAA\x90\x1F\x85')
		answ = self.verbindung.read(100)[3:7]
		self.clearInputBuffer()
		print(f"Seriennummer: {struct.unpack('>I', answ)[0]}")

	def setDataRate(self, newDataRate):
		cmd = b'\xAA\x94\x8B' + struct.pack('>f', newDataRate) + b'\x85'
		self.verbindung.write(cmd)
		self.clearInputBuffer()
		self.resetGSV6()

	def getFrame(self):
		FrameReceived = False
		praefix = self.verbindung.read(1)
		if praefix == b'\xAA':
			frame_id = self.verbindung.read(1)
			if frame_id == b'\x15':
				complete_frame = praefix + frame_id + self.verbindung.read(26)
				if complete_frame[-1:] == b'\x85':
					Frame = list(struct.unpack('>ffffff', complete_frame[3:27]))
					FrameReceived = True
			else:
				AnswFrame = praefix + frame_id + self.verbindung.read(int.from_bytes(frame_id, "big") - 78)
				if AnswFrame[-1:] == b'\x85':
					FrameReceived = True
					Frame = AnswFrame
		return FrameReceived, Frame

	def printAsHex(self, data):
		print(' '.join(format(x, '02x') for x in data))


if __name__ == '__main__':
	
	gsv = GSV6()
	gsv.stopTransmission()
	gsv.getSerNo()
	gsv.getDataRate()
	gsv.setDataRate(10)
	gsv.stopTransmission()
	gsv.getDataRate()
	gsv.startTransmission()

	start_time = time()
	cntr = 0
	while (time()-start_time) < 1:
		FrameReceived, MeasData = gsv.getFrame()
		if FrameReceived:
			print(f"Messwerte: {MeasData}")
			cntr += 1
	print(f"cntr: {cntr}")
	gsv.stopTransmission()
	gsv.close()
	print("\nProgrammende")
