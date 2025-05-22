#include <Adafruit_NeoPixel.h>

#define LED_PIN A5
#define LED_COUNT 64
Adafruit_NeoPixel leds(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

//colors
uint32_t ledWHITE = leds.Color(255, 255, 255);
uint32_t ledBLACK = leds.Color(0, 0, 0);
uint32_t ledRED   = leds.Color(255, 0, 0);
uint32_t ledGREEN = leds.Color(0, 255, 0);
uint32_t ledORANGE = leds.Color(255, 50, 0);
uint32_t ledYELLOW = leds.Color(255, 251, 0);
uint32_t ledBLUE = leds.Color(0, 0, 255);

//buttons
const int buttonPins[] = {5, 6, 7, 8, 9, 10, 11, 12};
const int buttonENTER = A1;
const int buttonCANCEL = 3;

//input buffer
char inputBuffer[5];
int inputIndex = 0;

//flashing
bool isFlashing = false;
int flashIndex = -1;
unsigned long lastFlashTime = 0;
bool flashState = false;
uint32_t flashColor = ledRED;

//cancelling
unsigned long lastCancelTime = 0;
unsigned long cancelPressCount = 0;
bool resetPromptActive = false;
uint32_t previousLEDColors[LED_COUNT];

//color transisitons - rainbow effect
unsigned long lastColorChange = 0;
int hue = 0;
int colorChangeSpeed = 10;

//breathing effect for leds
unsigned long lastBreathTime = 0;
int breathBrightness = 0;
int breathDirection = 1;
int breathSpeed = 20;

//quitting
unsigned long lastQuitTime = 0;
unsigned long quitPressCount = 0;
bool quitPromptActive = false;

//user input highlight
int highlightFromIndex = -1;
int highlightToIndex = -1;

void setup()
 {
  //connect to pi and show leds
  Serial.begin(9600);
  leds.begin();
  leds.setBrightness(90);
  leds.show();

  //buttons for enter and cancel
  pinMode(buttonENTER, INPUT_PULLUP);
  pinMode(buttonCANCEL, INPUT_PULLUP);

  //other buttons
  for (int i = 0; i < 8; i++)
  {
    pinMode(buttonPins[i], INPUT_PULLUP);
  }

  //rainbow startup
  startupRainbowEffect();
}

void loop() 
{
  //flash square if king is in check
  if (isFlashing && millis() - lastFlashTime > 500)
   {
    lastFlashTime = millis();
    flashState = !flashState;
    if (flashIndex >= 0 && flashIndex < LED_COUNT) 
    {
      leds.setPixelColor(flashIndex, flashState ? flashColor : ledBLACK);
      leds.show();
    }
  }

  //listen to pi messages
  if (Serial.available()) 
  {
    String response = Serial.readStringUntil('\n');
    response.trim();

    //if quit turn of all lights
    if(response == "QUIT")
    {
        startupRainbowEffect();
        for (int i = 0; i < LED_COUNT; i++) 
        {
          leds.setPixelColor(i, ledBLACK);
        }
      leds.show();
    }

    //if illegal move flash and wait a little bit
    if (response == "ILLEGAL")
    {
        //flash red
        for (int i = 0; i < LED_COUNT; i++) 
        {
            leds.setPixelColor(i, ledRED);
        }
        leds.show();
        delay(300);
        drawCheckerboard();
    }

    //if flash then flash
    if (response.startsWith("FLASH:")) 
    {
      String sq = response.substring(6);
      flashIndex = squareToIndex(sq);
      isFlashing = true;
    } 

    //if flash capture then flash capture
    else if (response.startsWith("FLASH_CAPTURE:")) 
    {
      String sq = response.substring(14);
      flashIndex = squareToIndex(sq);
      flashColor = ledRED;
      isFlashing = true;
    }

    //checkmate for ai win
    else if (response == "CHECKMATE:RED") 
    {
      for (int i = 0; i < LED_COUNT; i++) leds.setPixelColor(i, ledRED);
      leds.show();
    } 
    //checkmate for player win
    else if (response == "CHECKMATE:GREEN") 
    {
      for (int i = 0; i < LED_COUNT; i++) leds.setPixelColor(i, ledGREEN);
      leds.show();
    } 
    //reset
    else if (response == "RESET") 
    {
      isFlashing = false;
      flashIndex = -1;
      drawCheckerboard();
    } 
    //if the input is less than 4
    else if (response.length() >= 4)
    {
      String from = response.substring(0, 2);
      String to = response.substring(2, 4);
      drawCheckerboard();
      highlightMove(from, to);
    }
  }

  //button inputs
  for (int i = 0; i < 8; i++) 
  {
    if (digitalRead(buttonPins[i]) == LOW && inputIndex < 4) 
    {
      char c = mapButtonToChar(buttonPins[i], inputIndex);
      if (c != '?') 
      {
        inputBuffer[inputIndex++] = c;
        Serial.println(c);

        //highlight user move
        if (inputIndex == 2) 
        {
          String from = String(inputBuffer[0]) + String(inputBuffer[1]);
          highlightFromIndex = squareToIndex(from);
          leds.setPixelColor(highlightFromIndex, ledBLUE);
          leds.show();
        } 
        else if (inputIndex == 4) 
        {
          String to = String(inputBuffer[2]) + String(inputBuffer[3]);
          highlightToIndex = squareToIndex(to);
          leds.setPixelColor(highlightToIndex, ledYELLOW);
          leds.show();
        }

        delay(300);
        while (digitalRead(buttonPins[i]) == LOW);
      }
    }   
  }

  //enter button to submit
  if (digitalRead(buttonENTER) == LOW && inputIndex == 4) 
  {
      inputBuffer[4] = '\0';
      Serial.write(inputBuffer);
      Serial.write('\n');

      //reset highlights
      if (highlightFromIndex >= 0) 
      {
        int row = highlightFromIndex / 8;
        int col = highlightFromIndex % 8;
        leds.setPixelColor(highlightFromIndex, ((row + col) % 2 == 0) ? ledWHITE : ledBLACK);
      }

      if (highlightToIndex >= 0) 
      {
        int row = highlightToIndex / 8;
        int col = highlightToIndex % 8;
        leds.setPixelColor(highlightToIndex, ((row + col) % 2 == 0) ? ledWHITE : ledBLACK);
      }

      leds.show();

      inputIndex = 0;
      highlightFromIndex = -1;
      highlightToIndex = -1;
      memset(inputBuffer, 0, sizeof(inputBuffer));
      delay(500);
  }
  else if (digitalRead(buttonENTER) == LOW && resetPromptActive)
   {
        //user confuirmed reset
        resetPromptActive = false;
        cancelPressCount = 0;
        Serial.println("RESET");
        for (int i = 0; i < LED_COUNT; i++) leds.setPixelColor(i, ledBLACK);
        lightUpSequentially(ledGREEN); // Show confirmation with sequential LED light-up
        drawCheckerboard();
  }

  //cancel button
  if (digitalRead(buttonCANCEL) == LOW && !quitPromptActive)
  {
    unsigned long currentTime = millis();
    if (currentTime - lastCancelTime < 4000) 
    {  
      cancelPressCount++;
    } 
    else 
    {
      cancelPressCount = 1;
    }

    lastCancelTime = currentTime;

    if (cancelPressCount == 2 && !resetPromptActive) 
    {
      for (int i = 0; i < LED_COUNT; i++) 
      {
        previousLEDColors[i] = leds.getPixelColor(i);
      }

      for (int i = 0; i < LED_COUNT; i++) leds.setPixelColor(i, ledORANGE);
      leds.show();
      resetPromptActive = true;
      delay(500);
    }

    if (cancelPressCount == 1 && inputIndex > 0) 
    {
      if (highlightFromIndex >= 0) 
      {
        restoreTileColor(highlightFromIndex);
      }

      if (highlightToIndex >= 0) 
      {
        restoreTileColor(highlightToIndex);
      }

      leds.show();

      inputIndex = 0;
      highlightFromIndex = -1;
      highlightToIndex = -1;
      memset(inputBuffer, 0, sizeof(inputBuffer));

      Serial.write("CANCEL\n");
    }

    if (resetPromptActive) 
    {
      if (digitalRead(buttonCANCEL) == LOW) 
      {
        resetPromptActive = false;
        cancelPressCount = 0;
        for (int i = 0; i < LED_COUNT; i++) 
        {
          leds.setPixelColor(i, previousLEDColors[i]);
        }
        leds.show();
        delay(500);
      }
    }

    delay(500);
    while (digitalRead(buttonCANCEL) == LOW);
  }

  //quitting button sequence
  if (digitalRead(5) == LOW) 
  {
    unsigned long currentTime = millis();
    if (currentTime - lastQuitTime < 6000) 
    {
      quitPressCount++;
    } 
    else 
    {
      quitPressCount = 1;
    }

    lastQuitTime = currentTime;

    if (quitPressCount == 4 && !quitPromptActive) 
    {
      for (int i = 0; i < LED_COUNT; i++) 
      {
        previousLEDColors[i] = leds.getPixelColor(i);
      }

      for (int i = 0; i < LED_COUNT; i++) leds.setPixelColor(i, ledRED);
      leds.show();
      quitPromptActive = true;
      quitPressCount = 0;
      delay(500);
    }    
  }

  if (quitPromptActive) 
  {  
    if (digitalRead(buttonENTER) == LOW) 
    {
      Serial.println("quit");
      quitPromptActive = false;
      quitPressCount = 0;
      delay(500);
    } 
    else if (digitalRead(buttonCANCEL) == LOW) 
    {
      Serial.println("cancelled quitting");
      drawCheckerboard();
      quitPromptActive = false;
      quitPressCount = 0;
      delay(500);

      if (highlightFromIndex >= 0) 
      {
        restoreTileColor(highlightFromIndex);
      }

      if (highlightToIndex >= 0) 
      {
        restoreTileColor(highlightToIndex);
      }

      leds.show();

      inputIndex = 0;
      highlightFromIndex = -1;
      highlightToIndex = -1;
      memset(inputBuffer, 0, sizeof(inputBuffer));
      Serial.write("CANCEL\n");
    }
  }
}


//light up sequentially
void lightUpSequentially(uint32_t color) 
{
  for (int i = 0; i < LED_COUNT; i++) 
  {
    leds.setPixelColor(i, color);
    leds.show();
    delay(50);
  }
}

//button to char
char mapButtonToChar(int pin, int index) 
{
  if (index % 2 == 0)
   {
    switch (pin) 
    {
      case 5: return 'a';
      case 6: return 'b';
      case 7: return 'c';
      case 8: return 'd';
      case 9: return 'e';
      case 10: return 'f';
      case 11: return 'g';
      case 12: return 'h';
    }
  } else 
  {
    switch (pin) 
    {
      case 5: return '1';
      case 6: return '2';
      case 7: return '3';
      case 8: return '4';
      case 9: return '5';
      case 10: return '6';
      case 11: return '7';
      case 12: return '8';
    }
  }
  return '?';
}

//rile index based on square
int squareToIndex(String sq)
 {
  //flip this one so tis a to h
  int col = 7 - (sq.charAt(0) - 'a');

  //DO NOT FLIP
  int row = sq.charAt(1) - '1';

  if (row % 2 == 0) 
  {
    return row * 8 + col;            
  } else 
  {
    return row * 8 + (7 - col);       
  }
}

//restore original color
void restoreTileColor(int index) 
{
  int row = index / 8;
  int col = (row % 2 == 0) ? index % 8 : 7 - (index % 8);

  leds.setPixelColor(index, ((row + col) % 2 == 0) ? ledWHITE : ledBLACK);
}

//draw checkeboard
void drawCheckerboard() 
{
  for (int row = 0; row < 8; row++)
   {
    for (int col = 0; col < 8; col++) 
    {
      int index = (row % 2 == 0) ? row * 8 + col : row * 8 + (7 - col);
      leds.setPixelColor(index, ((row + col) % 2 == 0) ? ledWHITE : ledBLACK);
    }
  }
  leds.show();
}

//highlight move
void highlightMove(String from, String to) 
{
  int fromIndex = squareToIndex(from);
  int toIndex = squareToIndex(to);
  leds.setPixelColor(fromIndex, ledGREEN);
  leds.setPixelColor(toIndex, ledRED);
  leds.show();
}

//start up sequential effect
void startupSequentialEffect(uint32_t color) 
{
  for (int i = 0; i < LED_COUNT; i++) 
  {
    leds.setPixelColor(i, color); 
    leds.show();
    delay(50); 
  }

  delay(500); 
  for (int i = 0; i < LED_COUNT; i++) 
  {
    leds.setPixelColor(i, ledBLACK);
  }
  leds.show();
  
  drawCheckerboard();
}

void startupRainbowEffect() 
{
  uint32_t colors[] = 
  {
    //red
    leds.Color(255, 0, 0),
    //orange
    leds.Color(255, 100, 0),
    //yellow
    leds.Color(255, 255, 0),
    //green
    leds.Color(0, 255, 0),
    //blue
    leds.Color(0, 0, 255),
    //purple
    leds.Color(128, 0, 255)
  };
  int colorCount = sizeof(colors) / sizeof(colors[0]);

  for (int row = 0; row < 8; row++) 
  {
    for (int col = 0; col < 8; col++) 
    {
      int index = (row % 2 == 0) ? row * 8 + col : row * 8 + (7 - col);
      uint32_t color = colors[(index) % colorCount];
      leds.setPixelColor(index, color);
      leds.show();
      delay(50);
    }
  }

  delay(500);
  drawCheckerboard();
}