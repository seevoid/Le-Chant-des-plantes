#include <wiringPi.h>


#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

int main (void)
{
  int pin ;
  int dataPtr ;
  int l, s, d ;

  printf ("Raspberry Pi wiringPi test program\n") ;

  if (wiringPiSetup () == -1)
    exit (1) ;

  pinMode(7, INPUT) ;

  dataPtr = 0 ;

  while (1) {
  	float value = digitalRead(7);
  	printf("value %f \n", value);
  	sleep(3);
  }

  return 0 ;
}