int _ABVAR_1_GasSensor = 0;
int sensorValue = 0;
unsigned long myTime;

void setup()
{
  Serial.begin(9600);

// Alcohol sensor
#define Sober 300 
#define Drunk 500
#define MQ3 2
// Gas sensor
#define MQ2 0
}

void loop() {
//Print time
 Serial.print("Time: ");
 myTime = millis();
 Serial.println(myTime);

// Print alcohol sensor
int sensorValue = analogRead(MQ3); // read analog input pin 0
 Serial.print("Sensor Value: ");
 Serial.print(sensorValue);
if (sensorValue < Sober) {
    Serial.println("  |  Status: Sober");
  } else if (sensorValue >= Sober && sensorValue < Drunk) {
    Serial.println("  |  Status: Drinking but within legal limits");
  } else {
    Serial.println("  |  Status: DRUNK");
  }

// Print gas sensor
  _ABVAR_1_GasSensor = analogRead(MQ2) ;
  if (( ( _ABVAR_1_GasSensor ) > ( 100 ) ))
  {
    Serial.print("Gas/Fire detected");
    Serial.print(" ");
    Serial.print(_ABVAR_1_GasSensor);
    Serial.print(" ");
    Serial.println();
    delay(5000);
  }

  else
  {
    Serial.print("NO Gas/Fire");
    Serial.print(" ");
    Serial.print(_ABVAR_1_GasSensor);
    Serial.print(" ");
    Serial.println();
    delay(5000);
  }



}
