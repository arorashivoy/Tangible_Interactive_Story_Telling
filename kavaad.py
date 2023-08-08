import serial
import time
import RPi.GPIO as GPIO

################################################################################
# Global Variables
################################################################################
BUTTON_PIN_LEFT = 8
BUTTON_PIN_RIGHT = 12
SERVO_PIN = 11


################################################################################
# UIDs
################################################################################
# Flowers - 1
flower_uid = ['1de50441011080', '801de504410110', 'e504410110801d']

# Stories - 2 - Story1, Story2, Story3, Story4
story_block1_uid = ['1dc12441011080', '801dc124410110', 'c124410110801d']


# Characters - Monkey, Crocodile
monkey_uid = ['1d1e1441011080', '801d1e14410110', '1e14410110801d']
croc_uid = ['1d313441011080', '801d3134410110', '3134410110801d']

# Fruits - 3 - Mango, Apple, Pear
mango_uid = ['1d82e440011080', '801d82e4400110', '82e4400110801d']
apple_uid = ['1db0e540011080', '801db0e5400110', 'b0e5400110801d']
pear_uid = ['1dd5f440011080', '801dd5f4400110', 'd5f4400110801d']


################################################################################
# Functions
################################################################################
def move_lower_servo():
    ARDUINO_SERIAL1.write(b'1')
    time.sleep(0.055)


def read_successfully():
    for _ in range(90, 181, 5):
        move_lower_servo()

    for _ in range(180, 89, -5):
        move_lower_servo()


def move_upper_servo():
    global SERVO
    global duty, clockwise

    if duty == 7:
        clockwise = False
    elif duty == 2:
        clockwise = True

    if clockwise:
        duty += 1
    else:
        duty -= 1

    SERVO.ChangeDutyCycle(duty)
    time.sleep(0.13)


def speaking(narrator):
    global SERVO
    global clockwise
    if narrator == 1:
        move_upper_servo()

    elif narrator == 2:
        move_lower_servo()


def nfc_read():
    if ARDUINO_SERIAL1.inWaiting() > 0:
        uid = ARDUINO_SERIAL1.read(7)
        uid = uid.hex()
        print(str(uid))
        return str(uid)
    print("NO INPUT")
    return ""


def flush_nfc():
    ARDUINO_SERIAL1.flush()


def led_on(step: int, choice1: bool, choice2: bool):
    # Convert the variables to bytes
    step_bytes = str(step).encode()

    choice1_bytes = '1'.encode() if choice1 else '0'.encode()
    choice2_bytes = '1'.encode() if choice2 else '0'.encode()

    # Send the variables through the serial connection
    ARDUINO_SERIAL2.write(step_bytes + choice1_bytes + choice2_bytes)
    time.sleep(0.1)


################################################################################
# INIT and CLEANUP
################################################################################
def init():
    global SERVO
    global duty, clockwise
    global ARDUINO_SERIAL1, ARDUINO_SERIAL2

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(BUTTON_PIN_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(SERVO_PIN, GPIO.OUT)

    ARDUINO_SERIAL2 = serial.Serial('/dev/ttyUSB1', 115200)
    ARDUINO_SERIAL1 = serial.Serial('/dev/ttyUSB0', 115200)

    SERVO = GPIO.PWM(11, 50)
    SERVO.start(0)
    duty = 4
    clockwise = True

    ARDUINO_SERIAL1.flush()
    ARDUINO_SERIAL2.flush()
    time.sleep(1)


def cleanup():
    global SERVO
    led_on(0, 0, 0)

    ARDUINO_SERIAL1.close()
    ARDUINO_SERIAL2.close()
    SERVO.stop()

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
        if nfc_read() in story_block1_uid:
            read_successfully()
            return True
        return False

    # T2, 9
    elif screenIndex in [4, 16, 35, 39, 48, 56, 60, 64, 72, 78, 83, 91, 96]:
        if nfc_read() in monkey_uid:
            read_successfully()
            return True
        return False

    # T3, 8
    elif screenIndex in [6, 11, 20, 37, 43, 53, 62, 74, 80, 93]:
        if nfc_read() in croc_uid:
            read_successfully()
            return True
        return False

    # T4
    elif screenIndex in [8]:
        if nfc_read() in flower_uid:
            read_successfully()
            return True
        return False

    # T5
    elif screenIndex in [18, 100]:
        if nfc_read() in mango_uid:
            read_successfully()
            return True
        return False

    # T6
    elif screenIndex in [106]:
        if nfc_read() in apple_uid:
            read_successfully()
            return True
        return False

    # T7
    elif screenIndex in [103]:
        if nfc_read() in pear_uid:
            read_successfully()
            return True
        return False

    # For Choice Screen
    elif screenIndex in [25, 33, 77]:
        if GPIO.input(BUTTON_PIN_LEFT):
            return -1
        elif GPIO.input(BUTTON_PIN_RIGHT):
            return 1
        return 0
