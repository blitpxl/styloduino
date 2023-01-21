#include "Arduino.h"
#pragma once
#include "constants.h"

#define SOUND_OUTPUT_PIN 2

bool inrange(float voltage, float target)
{
  return (voltage < target + 0.025) && (voltage > target - 0.025);
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
  tone(SOUND_OUTPUT_PIN, note);
}

void stopTone()
{
  noTone(SOUND_OUTPUT_PIN);
}