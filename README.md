# CsgoGSI on Python and Arduino LCD shield

> A Counter-Strike: Global Offensive Game State Integration project based on python with screen on arduino

This project is using the [game state integration from csgo](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration). 
The informations are received by the program made in python and are shown on an arduino LCD shield.

### Features

- **Bomb timer (40s)**
- Health + kevlar bar
- Kills and headshots counter
- Money infoformations on buy time


## Table of Contents

- [Requirements](#requirements)
- [Install & Usage](#install--usage)
- [F.A.Q](#faq)


## Requirements

- [Python 3.x](https://www.python.org/downloads/) (tested on 3.6)
- pySerial package
Open a terminal : 

    ```sh
    pip --install pyserial 
    ```

- Arduino (tested on UNO rev3)
- Arduino LCD KeyPad Shield (tested on v1.1)
- USB Ports

### Do not forget
Verify if the pin are the good ones on the arduino program for the LCD shield. (line 10)

```cs
LiquidCrystal(rs, enable, d4, d5, d6, d7)
```

For LCD shield v1.0. Comment line 17-22 and uncomment line 24-30 in the serialsend.ino. Like this : 

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

## Install & Usage
0. Clone/download this git

1. Move gamestate_integration_arduinotrack.cfg in Program Files (x86)\Steam\SteamApps\common\Counter-Strike Global Offensive\csgo\cfg.

2. Mount the shield on the arduino (obviously) and [push](https://www.arduino.cc/en/main/howto) the serialsend.ino in the arduino (remember the COM port).

3. Launch CSGO

4. Run the python program

    ```sh
    python csgogsi.py
    ```

5. Enter the right COM like 'COM5'
    ```sh
    Ports availables : ['COM9', 'COM10']
    Please enter the corresponding COMX : COM9
    ```
6. Play some CSGO and enjoy!

## F.A.Q

1. The needed port (300 by default) is occupied. What should i do?

    Replace in csgogsi.py, line 195, col 33, the new corresponding port : 
    
    ```python
    SERVER = MyServer(('localhost', XXXREPLACEME), MyRequestHandler)
    ```
    
    And in gamestate_integration_arduinotrack.cfg, line 3 : 
    ```
    "uri" "http://127.0.0.1:XXXREPLACEME"
    ```

2. I don't understand what you've written!

    Sorry for my english. French is my primary language.
