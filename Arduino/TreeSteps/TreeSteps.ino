#include <FastLED.h>
#include <SoftwareSerial.h>

#define LED_PIN1     7
#define NUM_LEDS1    9

#define LED_PIN2     5
#define NUM_LEDS2    2

#define LED_PIN3     6
#define NUM_LEDS3    2

#define LED_PIN4     4
#define NUM_LEDS4    5

CRGB leds1[NUM_LEDS1];
CRGB leds2[NUM_LEDS2];
CRGB leds3[NUM_LEDS3];
CRGB leds4[NUM_LEDS4];

int step = 0;
int choice1 = 0;
int choice2 = 0;
bool ON = true;

void setup() {
  Serial.begin(115200);
  FastLED.addLeds<WS2812, LED_PIN1, GRB>(leds1, NUM_LEDS1);
  FastLED.addLeds<WS2812, LED_PIN2, GRB>(leds2, NUM_LEDS2);
  FastLED.addLeds<WS2812, LED_PIN3, GRB>(leds3, NUM_LEDS3);
  FastLED.addLeds<WS2812, LED_PIN4, GRB>(leds4, NUM_LEDS4);
  
}

void loop() {

   if (Serial.available() > 0) {
    int val = Serial.parseInt(); // Read the intger value
    int _choice2 = val % 10;
    val /= 10;
    int _choice1 = val % 10;
    val /= 10;
    int _step = val % 10;
    Serial.read(); // Read and discard the comma separator
    Serial.println(_step);
    Serial.println(_choice1);
    Serial.println(_choice2);

    if (_step >= 0 && _choice1 >= 0 && _choice2 >= 0) {
      step = _step;
      choice1 = _choice1;
      choice2 = _choice2;
    }

  }


  if (step == 0) {
    for (int i = 0; i < NUM_LEDS1; ++i) {
      leds1[i] = CRGB(0, 0, 0);
    }
    for (int i = 0; i < NUM_LEDS2; ++i) {
      leds2[i] = CRGB(0, 0, 0);
    }
    for (int i = 0; i < NUM_LEDS3; ++i) {
      leds3[i] = CRGB(0, 0, 0);
    }
    for (int i = 0; i < NUM_LEDS4; ++i) {
      leds4[i] = CRGB(0, 0, 0);
    }
    FastLED.show();

  }
  else if (step == 1 && choice1 == 1 && choice2 == 1) {
    leds4[4] = CRGB(0, 255, 0);
    leds3[1] = CRGB(0, 255, 0);
    leds2[1] = CRGB(0, 255, 0);
    leds1[8] = CRGB(0, 255, 0);
    FastLED.show();
  }
  else if (step == 1) {
    if (ON) {
      leds1[0] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds1[0] = CRGB(255, 200, 0);
  }
  if (step == 2) {
    leds1[0] = CRGB(0, 255, 0);
    if (ON) {
      leds1[1] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds1[1] = CRGB(255, 200, 0);
  }
  else if (step == 3) {
    leds1[1] = CRGB(0, 255, 0);
    if (ON) {
      leds1[2] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds1[2] = CRGB(255, 200, 0);
  }
  else if (step == 4) {
    leds1[2] = CRGB(0, 255, 0);
    if (ON) {
      leds1[3] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds1[3] = CRGB(255, 200, 0);
  }
  else if (step == 5 && !choice1) {
    leds1[3] = CRGB(0, 255, 0);
    if (ON) {
      leds1[4] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds1[4] = CRGB(255, 200, 0);
  }
  else if (step == 6 && !choice1) {
    leds1[4] = CRGB(0, 255, 0);
    if (ON) {
      leds1[5] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds1[5] = CRGB(255, 200, 0);
  }
  else if (step == 7 && !choice1) {
    leds1[5] = CRGB(0, 255, 0);
    if (ON) {
      leds1[6] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds1[6] = CRGB(255, 200, 0);
  }
  else if (step == 8 && !choice1 && !choice2) {
    leds1[6] = CRGB(0, 255, 0);
    if (ON) {
      leds1[7] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds1[7] = CRGB(255, 200, 0);
  }
  else if (step == 9 && !choice1 && !choice2) {
    leds1[7] = CRGB(0, 255, 0);
    if (ON) {
      leds1[8] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds1[8] = CRGB(255, 200, 0);
  }
  else if (step == 8 && !choice1 && choice2) {
    leds1[6] = CRGB(0, 255, 0);
    if (ON) {
      leds3[0] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds3[0] = CRGB(255, 200, 0);
  }
  else if (step == 9 && !choice1 && choice2) {
    leds3[0] = CRGB(0, 255, 0);
    if (ON) {
      leds3[1] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds3[1] = CRGB(255, 200, 0);
  }
  else if (step == 5 && choice1) {
    leds1[3] = CRGB(0, 255, 0);
    if (ON) {
      leds4[0] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds4[0] = CRGB(255, 200, 0);
  }
  else if (step == 6 && choice1) {
    leds4[0] = CRGB(0, 255, 0);
    if (ON) {
      leds4[1] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds4[1] = CRGB(255, 200, 0);
  }
  else if (step == 7 && choice1) {
    leds4[1] = CRGB(0, 255, 0);
    if (ON) {
      leds4[2] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds4[2] = CRGB(255, 200, 0);
  }
  else if (step == 8 && choice1 && !choice2) {
    leds4[2] = CRGB(0, 255, 0);
    if (ON) {
      leds2[0] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds2[0] = CRGB(255, 200, 0);
  }
  else if (step == 9 && choice1 && !choice2) {
    leds2[0] = CRGB(0, 255, 0);
    if (ON) {
      leds2[1] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds2[1] = CRGB(255, 200, 0);
  }
  else if (step == 8 && choice1 && choice2) {
    leds4[2] = CRGB(0, 255, 0);
    if (ON) {
      leds4[3] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds4[3] = CRGB(255, 200, 0);
  }
  else if (step == 9 && choice1 && choice2) {
    leds4[3] = CRGB(0, 255, 0);
    if (ON) {
      leds4[4] = CRGB(0, 0, 0);
    }
    FastLED.show();
    delay(300);
    ON = !ON;
    leds4[4] = CRGB(255, 200, 0);
  }

}

