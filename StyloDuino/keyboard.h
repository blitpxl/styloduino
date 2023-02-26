#pragma once
#include "Arduino.h"
#include "constants.h"

#define SOUND_OUTPUT_PIN 2

bool inrange(float voltage, float target)
{
  return (voltage < target + 0.03) && (voltage > target - 0.03);
}

int getKey(float voltage)
{
    for (int i = 0; i < 20; i++)
    {
        if (inrange(voltage, KEYS[i]))
        {
            return i;
        }
    }
}

void playTone(float note)
{
  if (SPK_ENABLED)
    tone(SOUND_OUTPUT_PIN, note);
}

void stopTone()
{
  noTone(SOUND_OUTPUT_PIN);
}

int skip_notes = 5;
int skipped = 0;

void SendByte(byte data)
{
  if (skipped < skip_notes)
  {
    skipped++;
  }
  else
  {
    Serial.write(data);
    skipped = 0;
  } 
}