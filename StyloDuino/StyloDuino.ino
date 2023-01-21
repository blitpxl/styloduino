#include "keyboard.h"

float value = 0.0;
float voltage = 0.0;

void setup(){ Serial.begin(9600); }

float getAnalogPinAverage(unsigned int pin, unsigned int sample)
{
  float values[sample] = {};
  float total = 0.0;
  
  for (int i = 0; i < sample; i++)
  {
    values[i] = (5.0/1023.0)*analogRead(pin);
  }
  for (float value : values)
  {
    total += value;
  }
  return (total / sample);
}


void loop() 
{
  voltage = getAnalogPinAverage(A0, 50);
  Serial.println(getKey(voltage));
  if (voltage > 0.1) 
  {
    switch (getKey(voltage))
    {
      case 0:
        playTone(KEY_A0);
        break;
      case 1:
        playTone(KEY_AS0);
        break;
      case 2:
        playTone(KEY_B0);
        break;
      case 3:
        playTone(KEY_C0);
        break;
      case 4:
        playTone(KEY_CS0);
        break;
      case 5:
        playTone(KEY_D0);
        break;
      case 6:
        playTone(KEY_DS0);
        break;
      case 7:
        playTone(KEY_E0);
        break;
      case 8:
        playTone(KEY_F0);
        break;
      case 9:
        playTone(KEY_FS0);
        break;
      case 10:
        playTone(KEY_G0);
        break;
      case 11:
        playTone(KEY_GS0);
        break;
      case 12:
        playTone(KEY_A1);
        break;
      case 13:
        playTone(KEY_AS1);
        break;
      case 14:
        playTone(KEY_B1);
        break;
      case 15:
        playTone(KEY_C1);
        break;
      case 16:
        playTone(KEY_CS1);
        break;
      case 17:
        playTone(KEY_D1);
        break;
      case 18:
        playTone(KEY_DS1);
        break;
      case 19:
        playTone(KEY_E1);
        break;
      default:
        break;
    }
  }
  else 
  {
    stopTone();
  }
}

