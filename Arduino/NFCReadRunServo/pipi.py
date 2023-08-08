import serial

ser = serial.Serial('/dev/ttyUSB0', 115200)  # Change '/dev/ttyUSB0' to the appropriate port for your system

while True:
    if ser.in_waiting > 0:
        uid_bytes = ser.read(7)  # Read the 7-byte UID as raw bytes
        print("Received UID:", uid_bytes.hex())
        if uid_bytes.hex() == '801d82e4400110':
            ser.write(b'1')