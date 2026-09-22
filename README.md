# KaavadBits — a tangible interactive storytelling installation

A tabletop installation that tells Panchatantra fables through a **Kaavad**, a
400-year-old Rajasthani storytelling object: a wooden shrine whose painted panels
fold open, one at a time, as the narrator recites. Here the Kaavad takes the form
of a tree, and the audience drives the branching story by placing carved wooden
tokens — a monkey, a crocodile, a mango, a flower — onto a reader in the trunk.

Published as **KaavadBits: Exploring Branching Narratives for Tangible Interactive
Storytelling through a Kaavad-inspired Diegetic Installation**, ACM TEI '24.
[doi:10.1145/3623509.3635251](https://doi.org/10.1145/3623509.3635251)

Saumik Shashwat\*, Aditya Padmagirwar\*, Shivoy Arora\*, Anmol Srivastava.
\*Three authors contributed equally.

> **A photograph of the built installation belongs here.** For a physical piece the
> object is the argument, and no amount of description substitutes for it.

## The idea

A conventional branching narrative asks you to press a button labelled "choice A".
This one asks you to hand the narrator a mango. The token *is* the choice, and it
is an object from the story world rather than an interface element sitting outside
it — that is what "diegetic" means here. Each token carries an NFC tag; reading the
tag both selects the branch and triggers the tree to physically open the next
panel, so the mechanism and the story advance together.

## Hardware

| Part | Role |
|---|---|
| Raspberry Pi | runs the story engine and drives the display and audio |
| Arduino + **PN532** NFC reader | reads token UIDs, reports them over serial at 115200 baud |
| Arduino + **FastLED** strip | lights the path up the tree as the story progresses |
| Servo on the Arduino (pin 9) | swings a panel open when a token reads successfully |
| Servo on Pi **board pin 11** | drives the second moving element |
| Two buttons, Pi board pins **8** and **12** | left and right choice, pulled down |
| Speaker | narration playback |

The two Arduinos appear to the Pi as `/dev/ttyUSB0` (LEDs) and `/dev/ttyUSB1` (NFC).
Note the pin numbers are **`GPIO.BOARD`** numbering, not BCM.

## Software

Three pieces, split by what they talk to:

- **`main.py`** — the story engine. A `Screen` class hierarchy models each beat of
  the narrative: `ScreenBut` waits on a button, `ScreenNFC` waits on a token,
  `ScreenAud` plays narration and advances when it finishes, `ScreenAudWait` plays
  and then waits for input. The story is a graph of these screens, rendered with
  pygame in portrait.
- **`kavaad.py`** — everything physical. Serial to both Arduinos, GPIO for the
  buttons and servo, and the **token UID table**: each carved token is a set of
  hex UIDs (the reader returns the bytes in different rotations, so every token
  lists several) mapped to a story element — flowers, the four story blocks, the
  monkey and crocodile characters, and the mango, apple and pear fruits.
- **`Arduino/`** — `NFCReadRunServo.ino` polls the PN532 and swings the servo on a
  successful read; `TreeSteps.ino` drives the LED strip.

The `test*.py` scripts at the top level each exercise one subsystem — LED, servo,
NFC, choice — which is how you bring the rig up when something is not responding.

## Running it

On the Raspberry Pi:

```sh
pip install pygame pyserial RPi.GPIO
python3 main.py
```

The display must be **portrait**. The Pi will not detect the orientation on its own
when running headless over VNC, so it has to be forced — copy `setup/config.txt`
over `/boot/config.txt` to force HDMI output at 1080x1920. See `setup/README.md`.

`RPi.GPIO` and the serial devices mean this only runs on the Pi with the rig
attached; it will not start on a laptop.
