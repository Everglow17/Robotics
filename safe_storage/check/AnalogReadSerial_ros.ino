
/*
  AnalogReadSerial
 .
*/
/* 
*  for some arduino broad, e.g. Arduino Micro, 
*  you must define USE_USBCON
*  to void errors when you're using rosserial
 */
#ifndef USE_USBCON
#define USE_USBCON
#endif

#include <FlexiTimer2.h>
#include <ros.h>
#include<std_msgs/Int32.h>

const int ledPin = 13; 
ros::NodeHandle  nh;

// the ROS message and the publisher
std_msgs::Int32 ir_data;
ros::Publisher pub("ir_data",&ir_data);

/*
 * period interrupt function
 */
 
void PIT()
{
// What is happening below? We read two values and store them in one number!?
// Why is that done? What do we have to do on the laptop? Why is that possible?
  ir_data.data = int32_t(averageAnalog(A5))<<16|averageAnalog(A4);
  pub.publish(&ir_data);
  nh.spinOnce();
}
// the setup routine runs once when you press reset:
void setup() {
  
  pinMode(ledPin, OUTPUT);
  
  nh.initNode();
  nh.advertise(pub);

 FlexiTimer2::set(2, PIT); 
 FlexiTimer2::start();
}

//We average the analog reading to elminate some of the noise
int averageAnalog(int pin){
  int v=0;
  for(int i=0; i<4; i++) v+= analogRead(pin);
  return v/4;
}

// the loop routine runs over and over again forever:
void loop() {
  
}
