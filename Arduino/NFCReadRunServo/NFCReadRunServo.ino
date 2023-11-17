#include <SoftwareSerial.h>
#include <PN532_SWHSU.h>
#include <PN532.h>
#include <Servo.h>

SoftwareSerial SWSerial( 3, 2 ); // RX, TX

Servo myServo;

int angle = 90;
bool clockwise = true;

PN532_SWHSU pn532swhsu( SWSerial );
PN532 nfc( pn532swhsu );

void moveServo(){
  if (angle == 90) {
    clockwise = true;
  }
  else if (angle == 180) {
    clockwise = false;
  }

  if (clockwise) {
    angle += 5;
  }
  else {
    angle -= 5;
  }
  myServo.write(angle);
  delay(60); 
}

void setup(void) {
  Serial.begin(115200);
  
  myServo.attach(9);
  myServo.write(90);
  
  nfc.begin();
  uint32_t versiondata = nfc.getFirmwareVersion();
  if (!versiondata) {
    Serial.print("Didn't find PN53x board");
    while (1);
  }
  nfc.SAMConfig();
}

void loop(void) {
  uint8_t success;
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };
  uint8_t uidLength;
  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength);

  if (success) {
    // Serial.write(uid, uidLength);// Send UID to the Raspberry Pi
    for (int i = 0; i < 36; ++i) {
        moveServo();
    }

    
    Serial.flush();
    delay(1);
  }

  // Check for incoming commands from the Raspberry Pi
  while (Serial.available() > 0) {
    char command = Serial.read(); // Read the incoming command
    // Process the command (in this case, the character '1' for servo movement)
    if (command == '1') {
      moveServo();
      Serial.flush();
    }
  }



    // for (int i = 0; i < 36; ++i) {
    //     moveServo();
    // }


  
}
