# GSV-6PI-Shield_example
In diesem Python-Script wird beispielhaft die Kommunikation mit dem GSV-6CPU über die serielle Schnittstelle auf einem 
Linux-Betriebssystem aufzeigt. Hierfür wird das Modul pyserial verwendet.
Über eine Lötbrücke kann beim GSV-6PI-Shield eingestellt werden, ob der GSV-6CPU bei Vorhandensein einer Spannung am 3,3 V – Pin 
des Raspberry PI (Pin 1) oder durch Aktivieren des GPIO12 (Pin 32), eingeschaltet werden soll. Wenn Letzteres ausgewählt wurde, 
muss zunächst mit Hilfe des RPi.GPIO – Moduls der Pin aktiviert werden bevor im nächsten Schritt eine serielle Verbindung 
aufgebaut wird. 
Folgende Parameter sind für die Konfiguration der seriellen Schnittstelle einzustellen:
Baudrate: 230400
Parity-Bit: None
Data-Bits: 8
Stop-Bits: 1	
Für die „Serial“-Methode reichen Angaben zum seriellen Port, zur Bautrate und zum Timeout aus. Im Terminal kann durch Eingabe 
des Befehls „dmesg | grep tty“ die serielle Schnittstelle gefunden werden.
Anschließend wird exemplarisch das Senden der Messwerte gestoppt, die Seriennummer angefordert und Versenden von Messwerten 
wieder gestartet. In welches Zahlenformat die Daten umgewandelt werden müssen, ist in der Protokollspezifikation für den GSV-6CPU 
(https://www.me-systeme.de/produkte/elektronik/gsv-8/anleitungen/ba-gsvcom..pdf) beschrieben. Im Python-Script sind zwei 
Funktionen hinterlegt, die zwischen den Zahlen und den Datenbytes konvertieren. Abschließend können Messwerte als Gleitkommazahl 
oder die vom GSV-6CPU empfangenen Messwert-Frames ausgegeben werden. Durch einen Keyboard-Interrupt wird die serielle Verbindung 
geschlossen und der GSV-6CPU ausgeschaltet.
