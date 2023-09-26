// Define pins
#define ALCOHOL_SENSOR 0
#define GAS_SENSOR 2

void setup()
{

Serial.begin(9600);

// Write header
Serial.print("Time(s), ")
Serial.print("Alcohol value, ")
Serial.print("Gas value, ")
Serial.println();

}

void loop() {

int gasvalue = analogRead(ALCOHOL_SENSOR);
int alcoholvalue = analogRead(GAS_SENSOR);

Serial.print(gasvalue);
Serial.print(" ");
Serial.print(alcoholvalue);
Serial.print(" ");
Serial.println();

}

