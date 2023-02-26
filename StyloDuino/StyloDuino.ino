// global variables
bool SPK_ENABLED = true;

#include "keyboard.h"

// local variables
float value = 0.0;
float voltage = 0.0;
int previous = 20;

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


void checkSpkToggle()
{
  int serial = Serial.read();
  if (serial > 0)
  {
    if (int(serial) - '0' == 1)
    {
      SPK_ENABLED = true;
    }
    else 
    {
      SPK_ENABLED = false;
    }
  }
}


void setup()
{
  Serial.begin(38400);
}


void loop() 
{
  voltage = getAnalogPinAverage(A0, 50);
  if (voltage > 0.1)
  {
    int key = getKey(voltage);
    int delta = (key - previous);
    previous = key;

    if (previous == 20)
      previous = key;
      
    if (delta < 5)
    {
      switch (key)
      {
        case 0:
          SendByte(0);
          playTone(KEY_A0);
          break;
        case 1:
          SendByte(1);
          playTone(KEY_AS0);
          break;
        case 2:
          SendByte(2);
          playTone(KEY_B0);
          break;
        case 3:
          SendByte(3);
          playTone(KEY_C0);
          break;
        case 4:
          SendByte(4);
          playTone(KEY_CS0);
          break;
        case 5:
          SendByte(5);
          playTone(KEY_D0);
          break;
        case 6:
          SendByte(6);
          playTone(KEY_DS0);
          break;
        case 7:
          SendByte(7);
          playTone(KEY_E0);
          break;
        case 8:
          SendByte(8);
          playTone(KEY_F0);
          break;
        case 9:
          SendByte(9);
          playTone(KEY_FS0);
          break;
        case 10:
          SendByte(10);
          playTone(KEY_G0);
          break;
        case 11:
          SendByte(11);
          playTone(KEY_GS0);
          break;
        case 12:
          SendByte(12);
          playTone(KEY_A1);
          break;
        case 13:
          SendByte(13);
          playTone(KEY_AS1);
          break;
        case 14:
          SendByte(14);
          playTone(KEY_B1);
          break;
        case 15:
          SendByte(15);
          playTone(KEY_C1);
          break;
        case 16:
          SendByte(16);
          playTone(KEY_CS1);
          break;
        case 17:
          SendByte(17);
          playTone(KEY_D1);
          break;
        case 18:
          SendByte(18);
          playTone(KEY_DS1);
          break;
        case 19:
          SendByte(19);
          playTone(KEY_E1);
          break;
        default:
          break;
      }
    }
  }
  else 
  {
    SendByte(20);
    stopTone();
  }
  checkSpkToggle();
}

