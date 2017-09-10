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
- Arduino (tested on UNO rev3)

- Arduino LCD KeyPad Shield (tested on v1.1)

- USB Ports

If you are not going to use Windows Binaries:

- [Python 3.x](https://www.python.org/downloads/) (tested on 3.6)

- pySerial package

    Open a terminal:

    ```sh
    pip install pyserial
    ```

    or, if anaconda installed:

    ```sh
    conda install pyserial
    ```

- qtpy package

    Open a terminal:

    ```sh
    pip install qtpy
    ```

    or, if anaconda installed:

    ```sh
    conda install qtpy
    ```

- PyQt5 or PyQt4 or PySide (tested with PyQt5)

    Open a terminal:

    ```sh
    pip install PyQt5
    ```

    ```sh
    pip install PyQt4
    ```

    ```sh
    pip install PySide
    ```

    or, if anaconda installed:

    ```sh
    conda install pyqt
    ```

    ```sh
    conda install pyside
    ```

### Do not forget

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

## Install & Usage

### Using portable binaries

1. Download windows/linux portable binaries

1. Move gamestate_integration_arduinotrack.cfg in Program Files (x86)\Steam\SteamApps\common\Counter-Strike Global Offensive\csgo\cfg.

1. Mount the shield on the arduino (obviously) and [push](https://www.arduino.cc/en/main/howto) the serialsend.ino in the arduino (remember the COM port)

1. Execute csgo-gsi-arduino-lcd

### Using from source

1. Clone/download this git

1. Move gamestate_integration_arduinotrack.cfg in Program Files (x86)\Steam\SteamApps\common\Counter-Strike Global Offensive\csgo\cfg.

1. Mount the shield on the arduino (obviously) and [push](https://www.arduino.cc/en/main/howto) the serialsend.ino in the arduino (remember the COM port).

1. Install the python program:

    ```sh
    pip install .
    ```

  Or manually:

    ```sh
    python setup.py install
    ```

1. Launch CSGO

1. Run the python program (choose one and make sure you have added /Python/Scripts to Path)

    Windows:

    ```sh
    csgogsilcd.bat
    ```

    Linux:

    ```sh
    csgogsilcd
    ```

    All:

    ```sh
    python csgogsilcd
    ```

1. Choose the right COM

1. Play some CSGO and enjoy!

## F.A.Q

1. The needed port (3000 by default) is occupied. What should i do?

    Replace in csgogsi.py, '3000' which is the default port (line 195, col 33) with the new corresponding port:

    ```python
    SERVER = MyServer(('localhost', 3000), MyRequestHandler)
    ```

    And in gamestate_integration_arduinotrack.cfg, line 3:
    ```cfg
    "uri" "http://127.0.0.1:3000"
    ```

1. Can i gather others informations than the ones proposed?

    Yes, you can. The out.txt is an example of the payload which is storing all the informations from CS:GO. For more information, you can follow this [guide](https://github.com/tsuriga/csgo-gsi-qsguide) and [the official wiki about CS:GO GSI](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration).
