// Reference https://innovatorsguru.com/zmct103c/

#include "EmonLib.h"

const long BAUDRATE = 2000000;
const float V_CALIBRATION = 234.26;
const float V_PHASE_SHIFT = 1.7;
const unsigned int V_SAMPLES_COUNT = 400; //default 1000
const float C_CALIBRATION = 570;
const unsigned int C_HALF_WAVELENGHT_COUNT = 10; //default 20
const unsigned int C_TIMEOUT = 2000; //deault 2000
const int SENSORS_COUNT = 6;

EnergyMonitor emon[SENSORS_COUNT];

void setup()
{
  Serial.begin(BAUDRATE);

  emon[0].voltage(0, V_CALIBRATION, V_PHASE_SHIFT);

  for (int i=0; i<SENSORS_COUNT; i++) {
    emon[i]=EnergyMonitor();
    emon[i].current(i, C_CALIBRATION);
  }
}

void loop()
{
  unsigned long start=micros();

  emon[0].calcVI(C_HALF_WAVELENGHT_COUNT,C_TIMEOUT);
  float vcc = emon[0].Vrms;

  for (int i=0; i<SENSORS_COUNT; i++) {
    unsigned long irms = emon[i].calcIrms(V_SAMPLES_COUNT);
    printToSerial(i, (int)vcc, (int)irms);
  }

  printExecutiontime(start);
}

void printExecutiontime(unsigned long start){
  unsigned long end=micros();
  unsigned long diff = end - start;
  Serial.print("t");
  Serial.println(diff/1000);
}

// Format plug_id,voltage(v),power(W), current(mA);
void printToSerial(int port, unsigned int Vcc, unsigned long Irms) {
  Serial.print(port);
  Serial.print(",");
  Serial.print(Vcc); //voltage
  Serial.print(",");
  Serial.print(Irms*Vcc/1000); // Apparent power
  Serial.print(",");
  Serial.print(Irms); // Irms
  Serial.print(";");
}
