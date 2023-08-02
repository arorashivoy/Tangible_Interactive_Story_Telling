import serial
import time
import RPi.GPIO as GPIO

################################################################################
# Global Variables
################################################################################
BUTTON_PIN_LEFT = 8
BUTTON_PIN_RIGHT = 12
ARDUINO_SERIAL1 = serial.Serial('/dev/ttyUSB1', 115200)
ARDUINO_SERIAL2 = serial.Serial('/dev/ttyUSB0', 115200)


################################################################################
# UIDs
################################################################################
# Flowers - 1
flower_uid = '20314420453520'

# Stories - 2 - Story1, Story2, Story3, Story4
story_block1_uid = '20314420433120'
story_block2_uid = '20314420353520'
#story_block3_uid = '20314420 '
#story_block4_uid = '20314420 '

# Characters - Monkey, Deer, Jackal, Elephant, Mouse, Lion, Crocodile, Crow - 8
monkey_uid = '20314420314520'
crow_uid = '20314420423220'
lion_uid = '2031442033120'
croc_uid = '20314420333120'
## dear_uid = '20314420 '
## jackal_uid = '20314420 '
## mouse_uid = '20314420 '
## tortoise_uid = '20314420 '

## Fruits - 3 - Mango, Apple, Pear 
mango_uid = '20314420383220'
apple_uid = '20314420423020'
pear_uid = '20314420443520'


################################################################################
# Functions
################################################################################
def move_servo():
	ARDUINO_SERIAL1.write(b'1')
	time.sleep(0.1)

def speaking(narrator):
	if narrator == 1:
		ARDUINO_SERIAL2.write('888'.encode())
	elif narrator == 2:
		ARDUINO_SERIAL1.write(b'1')
	time.sleep(0.1)

def nfc_read():
	if ARDUINO_SERIAL1.inWaiting() > 0:
		uid = ARDUINO_SERIAL1.read(7)
		uid = uid.hex()
		return str(uid)
	return ""


def led_on(step: int, choice1: bool, choice2: bool):
	# Convert the variables to bytes
	step_bytes = str(step).encode()
	
	choice1_bytes = '1'.encode() if choice1 else '0'.encode()
	choice2_bytes = '1'.encode() if choice2 else '0'.encode()
	
	# Send the variables through the serial connection
	ARDUINO_SERIAL2.write(step_bytes + choice1_bytes + choice2_bytes)
	time.sleep(0.1)
	

def init():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(BUTTON_PIN_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(BUTTON_PIN_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	ARDUINO_SERIAL1.flush()

def cleanup():
	ARDUINO_SERIAL1.close()
	ARDUINO_SERIAL2.close()
	GPIO.cleanup()



################################################################################
# Next Button
################################################################################
def check_next_botton(screenIndex):
	# For right button
	if screenIndex in []:
		return GPIO.input(BUTTON_PIN_RIGHT)
	


	# For left button
	if screenIndex in []:
		return GPIO.input(BUTTON_PIN_LEFT)
	


	# For nfc read screens
	# T1
	elif screenIndex in [2]:
		if nfc_read() == story_block1_uid:
			move_servo()
			return True
		return False
	
	# T2, 9
	elif screenIndex in [4, 35, 39, 48, 56, 60, 64, 72, 78, 83, 91, 96]:
		if nfc_read() == monkey_uid:
			move_servo()
			return True
		return False
	
	# T3, 8
	elif screenIndex in [6, 11, 20, 16, 37, 43, 53, 62, 74, 80, 93]:
		if nfc_read() == croc_uid:
			move_servo()
			return True
		return False
	
	# T4
	elif screenIndex in [8]:
		if nfc_read() == flower_uid:
			move_servo()
			return True
		return False
	
	# T5
	elif screenIndex in [18, 100]:
		if nfc_read() == mango_uid:
			move_servo()
			return True
		return False

	# T6
	elif screenIndex in [106]:
		if nfc_read() == apple_uid:
			move_servo()
			return True
		return False
	
	# T7
	elif screenIndex in [103]:
		if nfc_read() == pear_uid:
			move_servo()
			return True
		return False
	


	# For Choice Screen
	elif screenIndex in [25, 33, 77]:
		if GPIO.input(BUTTON_PIN_LEFT):
			return -1
		elif GPIO.input(BUTTON_PIN_RIGHT):
			return 1
		return 0