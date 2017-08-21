#include <LiquidCrystal.h>

#define btnRIGHT  0
#define btnUP     1
#define btnDOWN   2
#define btnLEFT   3
#define btnSELECT 4
#define btnNONE   5

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

int lcd_key     = 0;
int adc_key_in  = 0;

int read_LCD_buttons()
{
  // For V1.1 us this threshold
  if (adc_key_in < 50)   return btnRIGHT;  
  if (adc_key_in < 250)  return btnUP; 
  if (adc_key_in < 450)  return btnDOWN; 
  if (adc_key_in < 650)  return btnLEFT; 
  if (adc_key_in < 850)  return btnSELECT;  

  // For V1.0 comment the other threshold and use the one below:
  /*
    if (adc_key_in < 50)   return btnRIGHT;  
    if (adc_key_in < 195)  return btnUP; 
    if (adc_key_in < 380)  return btnDOWN; 
    if (adc_key_in < 555)  return btnLEFT; 
    if (adc_key_in < 790)  return btnSELECT;   
  */  
  return btnNONE;  // when all others fail, return this...
}

// Skull character
byte skull[8] = {
  0b01110,
  0b10101,
  0b11111,
  0b11011,
  0b01110,
  0b00000,
  0b01110,
  0b00000
};

byte HS[8] = {
  0b01110,
  0b11011,
  0b10001,
  0b11011,
  0b01110,
  0b00000,
  0b01110,
  0b00000
};

byte p1[8] = {
  0b10001,
  0x10,
  0x10,
  0x10,
  0x10,
  0x10,
  0x10,
  0b10001};

byte p2[8] = {
  0b11001,
  0x18,
  0x18,
  0x18,
  0x18,
  0x18,
  0x18,
  0b11001};

byte p3[8] = {
  0b11101,
  0x1C,
  0x1C,
  0x1C,
  0x1C,
  0x1C,
  0x1C,
  0b11101};

byte p4[8] = {
  0x1F,
  0x1E,
  0x1E,
  0x1E,
  0x1E,
  0x1E,
  0x1E,
  0x1F
};

byte p5[8] = {
  0x1F,
  0x1F,
  0x1F,
  0x1F,
  0x1F,
  0x1F,
  0x1F,
  0x1F};

byte empty[8] = {
  0b10001,
  0b00000,
  0b00000,
  0b00000,
  0b00000,
  0b00000,
  0b00000,
  0b10001
};

void setup() {
  lcd.createChar(0, skull);
  lcd.createChar(1, HS);
  lcd.createChar(2, p1);
  lcd.createChar(3, p2);
  lcd.createChar(4, p3);
  lcd.createChar(5, p4);
  lcd.createChar(6, p5);
  lcd.createChar(7, empty);
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.print("Start");
}

bool line2 = false;
void loop() {
  if (Serial.available() && !line2) {
    line2 = true; //switch line after
    delay(10);  // wait some time for the data to be fully  read
    lcd.clear();
    lcd.setCursor(0,0);
    while (Serial.available() > 0) {
      char c = Serial.read();
      lcd.write(c);
    }
  }
  else if (Serial.available() && line2) {
    line2 = false;
    delay(10);  // wait some time for the data to be fully  read
    lcd.setCursor(0,1);
    while (Serial.available() > 0) {
      char c = Serial.read();
      lcd.write(c);
    }
  }

  if (read_LCD_buttons() == btnSELECT) {
    lcd.clear();
  }
}
