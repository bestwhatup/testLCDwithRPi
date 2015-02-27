#!/usr/bin/env python
import RPi.GPIO as GPIO
import os
from time import sleep
from i2c_lcd_smbus import i2c_lcd #lib i2c - lcd

firsttime = 0
PB = 7
state = 0
count = 0

addr = 0x27 #addr i2c
port = 1
en   = 2
rw   = 1
rs   = 0
d4   = 4
d5   = 5
d6   = 6
d7   = 7
backlight = 3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PB,GPIO.IN)

lcd = i2c_lcd( addr, port, en, rw, rs, d4, d5, d6, d7, backlight ) #init lcd
lcd.backLightOn()
lcd.clear()
while True:
	if firsttime == 0 : #if firttime to run to show welcome
	    lcd.setPosition( 1, 0 )
	    lcd.writeString( "      Welcome" )
	    lcd.setPosition( 2, 0 )
	    lcd.writeString( "     Bestwhatup" )
	    lcd.setPosition( 3, 0 )
	    lcd.writeString( "  Push button Now!" )
	    inputValue = GPIO.input(PB) #fix get input

	inputValue = GPIO.input(PB)
	##### check status push button #####
	if state == 0 and inputValue == True :
		state = 1
	elif state == 1 and inputValue == False :
		count += 1
		firsttime = 1
		state = 0

	#if count = page cpu infomation
	if ((count % 2) == 0 and count != 0 and state != 1) :
		ex_command = os.popen("sudo cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq","r")
		current = ex_command.readline()
		ex_command = os.popen("vcgencmd measure_temp")
		temp = ex_command.readline()
		#fix refresh data not to clean lcd.
		if firsttime == 1:
			lcd.clear()
			firsttime = 2
			pass
		lcd.setPosition(1,2)
		lcd.writeString("Status RPi (cpu)")
		lcd.setPosition(2,0)
		lcd.writeString("CPU ferq : %s Mhz" %current[:3])
		lcd.setPosition(3,0)
		lcd.writeString("CPU temp : %s" %temp[5:11])
		lcd.setPosition(4,3)
		lcd.writeString("Push to back")
		inputValue = GPIO.input(PB)

	#if count = page memory infomation
	elif ((count % 2) == 1) :
		ex_command = os.popen("free")
		memory = ex_command.readlines()
		#fix refresh data not to clean lcd.
		if firsttime == 2:
			lcd.clear()
			firsttime = 1
			pass
		lcd.setPosition(1,2)
		lcd.writeString("Status RPi (ram)")
		lcd.setPosition(2,0)
		lcd.writeString("Mem total : %s Mb" %memory[1][13:16])
		lcd.setPosition(3,0)
		lcd.writeString("Mem used  : %s Mb" %memory[1][23:26])
		lcd.setPosition(4,3)
		lcd.writeString("Push to next")
		inputValue = GPIO.input(PB)
