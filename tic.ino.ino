#include <FastLED.h>

#define NUM_LEDS 60  // Number of LEDs in the strip
#define DATA_PIN 6   // Pin connected to the data line of the LED strip

CRGB leds[NUM_LEDS];

void setup() {
  Serial.begin(9600);
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
  FastLED.setBrightness(50);  // Set brightness to 50 (range is 0-255)
}

void loop() {
  if (Serial.available() > 0) {
    char received = Serial.read();
    if (received == 'X') {
      fill_solid(leds, NUM_LEDS, CRGB::Red);  // Set all LEDs to red
    } else if (received == 'O') {
      fill_solid(leds, NUM_LEDS, CRGB::Blue);  // Set all LEDs to blue
    } else if (received == 'W') {
      fill_solid(leds, NUM_LEDS, CRGB::Green);  // Set all LEDs to green for X win
    } else if (received == 'L') {
      fill_solid(leds, NUM_LEDS, CRGB::Green);  // Set all LEDs to green for O win
    }
    FastLED.show();
  }
}
