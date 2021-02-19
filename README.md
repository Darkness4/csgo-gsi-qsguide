# CsgoGSI on Python and Arduino LCD shield

> A Counter-Strike: Global Offensive Game State Integration project based on python with screen on arduino

This project is using the [game state integration from csgo](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration).
The informations are received by the program made in python and are shown on an arduino LCD shield.

### Features

-   **Bomb timer (40s)**
-   Health + kevlar bar
-   Kills and headshots counter
-   Money informations on buy time

## Table of Contents

-   [Requirements](#requirements)
-   [Install & Usage](#install--usage)
-   [F.A.Q](#faq)

## Requirements
-   Arduino (tested on UNO rev3)
-   Arduino LCD KeyPad Shield (tested on v1.1)
-   USB Ports
-   [Python 3.8+](https://www.python.org/downloads/)

### Check the pins in Arduino

Verify if the pin are the good ones on the arduino program for the LCD shield. (line 10)

```cs
LiquidCrystal(rs, enable, d4, d5, d6, d7)
```

For LCD shield v1.0. Comment line 17-22 and uncomment line 24-30 in the serialsend.ino. Like this:

```cs
  // For V1.1 us this threshold
  /*
  if (adc_key_in < 50)   return btnRIGHT;
  if (adc_key_in < 250)  return btnUP;
  if (adc_key_in < 450)  return btnDOWN;
  if (adc_key_in < 650)  return btnLEFT;
  if (adc_key_in < 850)  return btnSELECT;
  */
  // For V1.0 comment the other threshold and use the one below:
  if (adc_key_in < 50)   return btnRIGHT;
  if (adc_key_in < 195)  return btnUP;
  if (adc_key_in < 380)  return btnDOWN;
  if (adc_key_in < 555)  return btnLEFT;
  if (adc_key_in < 790)  return btnSELECT;
```

## Usage

1. Clone/download this repository :

   ```sh
   git clone git@github.com:Darkness4/csgo-gsi-arduino-lcd.git
   ```

1. Move *gamestate_integration_arduinotrack.cfg* in *Counter-Strike Global Offensive\csgo\cfg*.

1. Mount the LCD shield on the arduino and [push](https://www.arduino.cc/en/main/howto) the *serialsend.ino* in the arduino (remember the COM port).

1. Install the dependencies:

   - Using pip :

     ```sh
     pip install -r requirements.txt
     ```

   - Using pipenv :

     ```sh
     pipenv install
     pipenv shell
     ```

5. Launch CS:GO

6. Run the python program (choose one and make sure you have added /Python/Scripts to Path)

   ```sh
   python -m csgo_gsi_arduino_lcd
   ```

7. Choose the right COM

8. Play some CSGO and enjoy!