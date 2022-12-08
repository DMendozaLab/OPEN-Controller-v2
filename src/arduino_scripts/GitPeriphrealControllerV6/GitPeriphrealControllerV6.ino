/* This code was written on 9/8/2020 by Maria Lusardi for BIPS
    It utilizes many functions that were in the previous version of PeriphrealControllerCode, but alters the ParseCommand function
    It is intended to control the growlights and the backlights in the Sunbear independently.
    It can only control whether the lights are on or off, the color is set at a constant Bluewhite = (180, 210, 180) and the brightness is set to 180.
*/

/* Code Revised 10/7/2020 Landon Swartz
    - Changed strip on or off boolean expression to compare to a int value of 1 and not '1' (char of 1)
    - Removed read success serial comment from loop() then added delay(10) to ease up serial communication timing
    - Fixed spelling error of recieved in loop()
*/
#include <Adafruit_NeoPixel.h>

#ifdef __AVR__
#include <avr/power.h>
#endif

#define NEOPIN_0 2
#define NEOPIN_1 3
#define NEOPIN_2 4
#define NEOPIN_3 5
#define NEOPIN_4 6

#define GROWLIGHT 9
#define INPUT_SIZE 30
#define BRIGHTNESS 180

//declaring strips
Adafruit_NeoPixel strip_0 = Adafruit_NeoPixel(75, NEOPIN_0);
Adafruit_NeoPixel strip_1 = Adafruit_NeoPixel(75, NEOPIN_1);
Adafruit_NeoPixel strip_2 = Adafruit_NeoPixel(75, NEOPIN_2);
Adafruit_NeoPixel strip_3 = Adafruit_NeoPixel(75, NEOPIN_3);
Adafruit_NeoPixel strip_4 = Adafruit_NeoPixel(75, NEOPIN_4);

//declaring colors
uint32_t color_0 = strip_0.Color(180, 210, 180);
uint32_t color_1 = strip_1.Color(180, 210, 180);
uint32_t color_2 = strip_2.Color(180, 210, 180);
uint32_t color_3 = strip_3.Color(180, 210, 180);
uint32_t color_4 = strip_4.Color(180, 210, 180);

bool lightsOn = false;

void setup() {
  //Neostrip start-up, initialize pins, turn off
  Serial.println("arduino on");

#if defined (__AVR_ATtiny85__)
  if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
#endif

  Serial.begin(115200);
  pinMode(GROWLIGHT, OUTPUT);
  digitalWrite(GROWLIGHT, HIGH);

  strip_begin();
  strip_show();
}

void strip_begin()
{
  strip_0.begin();
  strip_1.begin();
  strip_2.begin();
  strip_3.begin();
  strip_4.begin();
}

void strip_show()
{
  strip_0.show();
  strip_1.show();
  strip_2.show();
  strip_3.show();
  strip_4.show();
}

void loop() {
  // Recieve command string, parse it, and execute
  char inData[INPUT_SIZE + 1];
  int index = 0;
  Serial.flush();

  while (Serial.available() > 0) {
    char recieved = Serial.read(); //Serial.read() only reads one character at a time
    inData[index++] = recieved; //As each character is received, it is added to the character array inData, which can hold a string of length 30
    delay(10); //for serial port to read in data in reasonable timing

    // Process message when the end of the string is encountered
    if (recieved == '\n')
    {
      Serial.print("Arduino Received: ");
      Serial.print(inData);
      parseCommand(inData); //interprets the command and decides what to do with it
      memset(&inData[0], 0, sizeof(inData)); //clears the array, sets all index values to 0
      index = 0; //resets index to 0
    }
  }
}

//Changes bool value of a given pin
void togglePin(int pin, bool value) {
  digitalWrite(pin, value);
}

//Changes the bool value of the neostrip strip to determine if on or off
void toggleStrip(bool val) {
  (val == 1) ? stripOn() : stripOff();
}

//Turns neopixel strip (backlights) on
void stripOn() {
  
  strip_0.setBrightness(BRIGHTNESS);
  strip_0.fill(color_0);
  strip_0.show();

  strip_1.setBrightness(BRIGHTNESS);
  strip_1.fill(color_1);
  strip_1.show();

  strip_2.setBrightness(BRIGHTNESS);
  strip_2.fill(color_2);
  strip_2.show();

  strip_3.setBrightness(BRIGHTNESS);
  strip_3.fill(color_3);
  strip_3.show();

  strip_4.setBrightness(BRIGHTNESS);
  strip_4.fill(color_4);
  strip_4.show();
  
  lightsOn = true;
}

//Turns neopixel strip (backlights) off
void stripOff() {
  strip_clear();
  strip_show();
  lightsOn = false;
}

void strip_clear()
{
  strip_0.clear();
  strip_1.clear();
  strip_2.clear();
  strip_3.clear();
  strip_4.clear();
}

//Converts characters to bools
bool ctob (char value) {
  return (value == '1') ? true : false;
}

//Converts characters to integers
int ctoi (char integer) {
  return integer - '0';
}

//Prints error messages to the serial port
void printError() {
  Serial.println("Unknown Command Received");
}

//This function turns the grow lights on and off (they are not neopixels)
void handleGrowLightSwitch(char* cmdString) {
  char value = cmdString[3];
  togglePin(GROWLIGHT, ctob(value)); //high turns on relay because normally open, so stops off relay
}

//This function turns the backlight on and off (they are neopixels)
void handleToggleNP(char* cmdString) {
  char value = cmdString[3];
  toggleStrip(ctob(value));
}

//Resets the character pointer of a string to begin at 'S', in case the comand string doesn't already start at 'S'
//Will return NULL if 'S' is not found in the string
char* sanatizeCommand(char* cmdStr) {
  char* cleanStr = strchr(cmdStr, 'S');
  return cleanStr;
}

void parseCommand(char* cmdString) {
  cmdString = sanatizeCommand(cmdString);
  char mode = cmdString[0];
  char cmdType = cmdString[1];

  switch (mode) {
    case 'S':
      switch (cmdType) {
        case '1':
          handleGrowLightSwitch(cmdString);
          break;
        case '2':
          handleToggleNP(cmdString);
          break;
        default:
          printError();
      }
      break;
    default:
      printError();
  }
}
