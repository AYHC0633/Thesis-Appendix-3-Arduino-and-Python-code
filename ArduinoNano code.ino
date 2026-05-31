/*!
Linear Technology DC2091A Demonstration Board.
LTC5599: 130 to 1300MHz IQ Modulator. <---sister board of LTC5589

@verbatim

NOTES
  Setup:
   Set the terminal baud rate to 115200 and select the newline terminator.

USER INPUT DATA FORMAT:
 decimal : 1024
 hex     : 0x400
 octal   : 02000  (leading 0 "zero")
 binary  : B10000000000
 float   : 1024.0

@endverbatim

http://www.linear.com/product/LTC5599

http://www.linear.com/product/LTC5599#demoboards


Copyright 2018(c) Analog Devices, Inc.

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
 - Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
 - Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in
   the documentation and/or other materials provided with the
   distribution.
 - Neither the name of Analog Devices, Inc. nor the names of its
   contributors may be used to endorse or promote products derived
   from this software without specific prior written permission.
 - The use of this software may or may not infringe the patent rights
   of one or more patent holders.  This license does not release you
   from the requirement that you obtain separate licenses from these
   patent holders to use this software.
 - Use of the software either in source or binary form, must be run
   on or directly connected to an Analog Devices Inc. component.

THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT,
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, INTELLECTUAL PROPERTY RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

/*! @file
    @ingroup LTC5599
*/

// Function Declaration
#include <Arduino.h>
#include <stdint.h>
#include "Linduino.h" /*keyword: QUIKEVAL_CS = SS; --> pin10 in Arduino Uno , QUIKEVAL_MUX_MODE_PIN == 8 */
#include "LT_SPI.h"
#include "UserInterface.h"
#include "LT_I2C.h"
#include "QuikEval_EEPROM.h"
#include "LTC5599.h"  //Library are bascially the same (I think)
#include <SPI.h>      // keyword: SPI_CLOCK_DIV16 = 0x01
#include <Wire.h>

//Global variables

uint8_t rw;
uint8_t readback_byte;
uint8_t write_byted_init0[] = {0x40,0xA0,0x13,0x13,0x80,0x10,0x50,0x60,0x00};//0x97,0xff
uint8_t write_byted30[] = { 0x40, 0x01, 0x3B, 0x01, 0x80, 0x10, 0x50, 0x06, 0x00 };
uint8_t Qshift[] = { 0x21, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x25, 0x4E, 0x73, 0x9B, 0xC8, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xd7, 0xA9, 0x87, 0x67, 0x46, 0x21 };
uint8_t Ishift[] = { 0x01, 0x15, 0x3B, 0x5A, 0x76, 0x94, 0xB8, 0xEA, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xF6, 0xC3, 0x96, 0x6F, 0x46, 0x16, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01 };

uint8_t Qshift1[] = { 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
                      0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
                      0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x05, 0x07, 0x09, 0x0b, 0x0d, 0x0f, 0x11, 0x13, 0x15, 0x17, 0x19, 0x1b, 0x1d,
                      0x1f, 0x21, 0x23, 0x25, 0x27, 0x29, 0x2b, 0x2d, 0x2f, 0x31, 0x33, 0x35, 0x37, 0x39, 0x3b, 0x3d, 0x3f, 0x41, 0x43, 0x45, 0x47, 0x49, 0x4b, 0x4d, 0x4f,
                      0x51, 0x53, 0x55, 0x57, 0x59, 0x5b, 0x5d, 0x5f, 0x61, 0x63, 0x65, 0x67, 0x69, 0x6b, 0x6d, 0x6f, 0x71, 0x73, 0x75, 0x77, 0x79, 0x7b, 0x7d, 0x7f, 0x81,
                      0x83, 0x85, 0x87, 0x89, 0x8b, 0x8d, 0x8f, 0x91, 0x93, 0x95, 0x97, 0x99, 0x9b, 0x9d, 0x9f, 0xa1, 0xa3, 0xa5, 0xa7, 0xa9, 0xab, 0xad, 0xaf, 0xb1, 0xb3,
                      0xb5, 0xb7, 0xb9, 0xbb, 0xbd, 0xbf, 0xc1, 0xc3, 0xc5, 0xc7, 0xc9, 0xcb, 0xcd, 0xcf, 0xd1, 0xd3, 0xd5, 0xd7, 0xd9, 0xdb, 0xdd, 0xdf, 0xe1, 0xe3, 0xe5,
                      0xe7, 0xe9, 0xeb, 0xed, 0xef, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                      0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                      0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xf0, 0xee, 0xec, 0xea, 0xe8, 0xe6, 0xe4, 0xe2, 0xe0, 0xde,
                      0xdc, 0xda, 0xd8, 0xd6, 0xd4, 0xd2, 0xd0, 0xce, 0xcc, 0xca, 0xc8, 0xc6, 0xc4, 0xc2, 0xc0, 0xbe, 0xbc, 0xba, 0xb8, 0xb6, 0xb4, 0xb2, 0xb0, 0xae, 0xac,
                      0xaa, 0xa8, 0xa6, 0xa4, 0xa2, 0xa0, 0x9e, 0x9c, 0x9a, 0x98, 0x96, 0x94, 0x92, 0x90, 0x8e, 0x8c, 0x8a, 0x88, 0x86, 0x84, 0x82, 0x80, 0x7e, 0x7c, 0x7a,
                      0x78, 0x76, 0x74, 0x72, 0x70, 0x6e, 0x6c, 0x6a, 0x68, 0x66, 0x64, 0x62, 0x60, 0x5e, 0x5c, 0x5a, 0x58, 0x56, 0x54, 0x52, 0x50, 0x4e, 0x4c, 0x4a, 0x48,
                      0x46, 0x44, 0x42, 0x40, 0x3e, 0x3c, 0x3a, 0x38, 0x36, 0x34, 0x32, 0x30, 0x2e, 0x2c, 0x2a, 0x28, 0x26, 0x24, 0x22, 0x20, 0x1e, 0x1c, 0x1a, 0x18, 0x16,
                      0x14, 0x12, 0x10, 0x0e, 0x0c, 0x0a, 0x08, 0x06, 0x04, 0x02 };
uint8_t Ishift1[] = { 0x01, 0x03, 0x05, 0x07, 0x09, 0x0b, 0x0d, 0x0f, 0x11, 0x13, 0x15, 0x17, 0x19, 0x1b, 0x1d, 0x1f, 0x21, 0x23, 0x25, 0x27, 0x29, 0x2b, 0x2d, 0x2f, 0x31,
                      0x33, 0x35, 0x37, 0x39, 0x3b, 0x3d, 0x3f, 0x41, 0x43, 0x45, 0x47, 0x49, 0x4b, 0x4d, 0x4f, 0x51, 0x53, 0x55, 0x57, 0x59, 0x5b, 0x5d, 0x5f, 0x61, 0x63,
                      0x65, 0x67, 0x69, 0x6b, 0x6d, 0x6f, 0x71, 0x73, 0x75, 0x77, 0x79, 0x7b, 0x7d, 0x7f, 0x81, 0x83, 0x85, 0x87, 0x89, 0x8b, 0x8d, 0x8f, 0x91, 0x93, 0x95,
                      0x97, 0x99, 0x9b, 0x9d, 0x9f, 0xa1, 0xa3, 0xa5, 0xa7, 0xa9, 0xab, 0xad, 0xaf, 0xb1, 0xb3, 0xb5, 0xb7, 0xb9, 0xbb, 0xbd, 0xbf, 0xc1, 0xc3, 0xc5, 0xc7,
                      0xc9, 0xcb, 0xcd, 0xcf, 0xd1, 0xd3, 0xd5, 0xd7, 0xd9, 0xdb, 0xdd, 0xdf, 0xe1, 0xe3, 0xe5, 0xe7, 0xe9, 0xeb, 0xed, 0xef, 0xff, 0xff, 0xff, 0xff, 0xff,
                      0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                      0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                      0xff, 0xff, 0xff, 0xff, 0xff, 0xf0, 0xee, 0xec, 0xea, 0xe8, 0xe6, 0xe4, 0xe2, 0xe0, 0xde, 0xdc, 0xda, 0xd8, 0xd6, 0xd4, 0xd2, 0xd0, 0xce, 0xcc, 0xca,
                      0xc8, 0xc6, 0xc4, 0xc2, 0xc0, 0xbe, 0xbc, 0xba, 0xb8, 0xb6, 0xb4, 0xb2, 0xb0, 0xae, 0xac, 0xaa, 0xa8, 0xa6, 0xa4, 0xa2, 0xa0, 0x9e, 0x9c, 0x9a, 0x98,
                      0x96, 0x94, 0x92, 0x90, 0x8e, 0x8c, 0x8a, 0x88, 0x86, 0x84, 0x82, 0x80, 0x7e, 0x7c, 0x7a, 0x78, 0x76, 0x74, 0x72, 0x70, 0x6e, 0x6c, 0x6a, 0x68, 0x66,
                      0x64, 0x62, 0x60, 0x5e, 0x5c, 0x5a, 0x58, 0x56, 0x54, 0x52, 0x50, 0x4e, 0x4c, 0x4a, 0x48, 0x46, 0x44, 0x42, 0x40, 0x3e, 0x3c, 0x3a, 0x38, 0x36, 0x34,
                      0x32, 0x30, 0x2e, 0x2c, 0x2a, 0x28, 0x26, 0x24, 0x22, 0x20, 0x1e, 0x1c, 0x1a, 0x18, 0x16, 0x14, 0x12, 0x10, 0x0e, 0x0c, 0x0a, 0x08, 0x06, 0x04, 0x02,
                      0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
                      0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
                      0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01 };
uint8_t address[] = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,0x08};
int ii = 1;


//-----------------------------layer numer identifier
  int arraynum[] = {0,1,2,3,4,5,6,7,
                   16,17,18,19,20,21,22,23,
                   32,33,34,35,36,37,38,39,
                   48,49,50,51,52,53,54,55,
                   64,65,66,67,68,69,70,71,
                   80,81,82,83,84,85,86,87,
                   96,97,98,99,100,101,102,103,
                   112,113,114,115,116,117,118,119
                   };




int test = 0;



//DAC data for sin wave

// --------------Data formatting 
union
  {
    uint8_t Valbyte[2];
    uint16_t fullword;
  } IValu, QValu;

uint8_t write_byte[18];

bool UpdateFlag = false; 

//! Initialize Linduino

//---------------global Variable 
int SPIupdateSpeed = 6;
int I2CupdateSpeed = 4;

void setup() {

  
  char demo_name[] = "DC2091";  //!< Demo Board Name stored in QuikEval EEPROM
                                //quikeval_I2C_init();           // Configure the EEPROM I2C port for 100kHz <----useless since the chip only support SPI it seem, will test it later

  //-------------------------------------SPI connection from Arduino to LTC5589  setting
  SPI.begin();
  SPI.setClockDivider(SPI_CLOCK_DIV16);  // Configure the spi port for 4MHz SCK

  pinMode(QUIKEVAL_CS, OUTPUT);     // chip select, pin 10
  digitalWrite(QUIKEVAL_CS, HIGH);  //  chip select, pin 10

  pinMode(QUIKEVAL_MUX_MODE_PIN, OUTPUT);    // Connect SPI to main data port, pin 8 MOSI
  digitalWrite(QUIKEVAL_MUX_MODE_PIN, LOW);  // Connect SPI to main data port, pin 8
  


  Serial.begin(115200);  // Initialize the serial port to the PC
  

 //-----------------------------------CD74HC154
    pinMode(2, OUTPUT);  // A0  
    pinMode(3, OUTPUT);  // A1
    pinMode(4, OUTPUT);  // A2    
    pinMode(5, OUTPUT);  // A3     
    pinMode(6, OUTPUT);  // A4     
    pinMode(7, OUTPUT);  // A5   
    pinMode(8, OUTPUT);  // A6     
    pinMode(9, OUTPUT);  // A7
    pinMode(A0, OUTPUT);  // E1  
    pinMode(A1, OUTPUT);  // E2  

 

//-------------------------------------I2C connection from Arduino to Raspberry  setting
  Wire.begin(0x0a);
  Wire.onReceive(Eventt);  // Code reference from DroneBot Workshop
  rw = 0x00;  // write
  
  

    
  delay(SPIupdateSpeed); 

  //--------------All unitcell on layer initialize 
  for (int ii = 0 ; ii<=63;ii++){
    initset(ii);
  };
  initset(0);
 
  
  
}
int swi = 1;
void loop() {
  
//---------------main code
  if(UpdateFlag == true){
    if (swi == 1){
      Serial.println("Update on unitcell ");
      if(write_byte[15]<9){
        singleIQupdate();
      }else if(write_byte[15]==9){
        IQUpdate();
      }else if(write_byte[15]==10){
        DACUpdate();
      }
      else{
        IQUpdate();
        DACUpdate();
      };
      swi = 2;
    }
    else{
    Serial.println("Swapping unitcell");
     if(write_byte[15]<9){
        singleIQupdate();
      }else if(write_byte[15]==9){
        IQUpdate();
        
      }else if(write_byte[15]==10){
        DACUpdate();
      }
     else{
        IQUpdate();
        DACUpdate();
     };
    swi = 1;
    }
    Serial.println("I2CupdateEnd---------");
    UpdateFlag = false; 
  }
  
}

//--------------------------I2C event
void Eventt(int numBytesRemain) {
  
  if(UpdateFlag == false){
    int i = 0;
    while (Wire.available()) {
      write_byte[i] = Wire.read();
      i++;
    }
    UpdateFlag = true;
  }
  else{
    // if there is overwrite while Slave Reading, trash that data!
    while (Wire.available()) {
      byte trash = Wire.read();
    }
  }
}

//--------------CD74HC154---------

void chipselect(int trigger,int NanoNum){
  
  digitalWrite(2, bitRead(NanoNum,0));
  digitalWrite(3, bitRead(NanoNum,1));    
  digitalWrite(4, bitRead(NanoNum,2));    
  digitalWrite(5, bitRead(NanoNum,3)); 
  digitalWrite(6, bitRead(NanoNum,4));    
  digitalWrite(7, bitRead(NanoNum,5));    
  digitalWrite(8, bitRead(NanoNum,6)); 
  digitalWrite(9, bitRead(NanoNum,7)); 
  delay(I2CupdateSpeed);
  digitalWrite(A0,trigger); 
  digitalWrite(A1,trigger); 
  delay(I2CupdateSpeed);
}

void chipCSBclose(){
  delay(I2CupdateSpeed);  
  digitalWrite(A0,1); 
  digitalWrite(A1,1); 
  delay(I2CupdateSpeed);  
}

//-----------------------------------IQ Update ------------------------------
void IQUpdate(){
 // int Unitsel1 = 0;//int UN = write_byte[1];
 int Unitsel1 = write_byte[0];
 Serial.println(Unitsel1);
 Serial.println("/n");
  for (int i = 1; i <=8; i++)  // i2C cant sent 0x00 in the line, so address 0x08 will not be written!!!
  {
    chipselect(0,arraynum[Unitsel1]);
    LTC5599_write_read(LTC5599_CS, address[i], rw, write_byte[i], &readback_byte);
    delay(I2CupdateSpeed);
    chipCSBclose();
    Serial.println(write_byte[i]);
    delay(I2CupdateSpeed);
  }
  Serial.println("---IQEnd /n");
};

void singleIQupdate(){
  int Unitsel1 = write_byte[0];
  int IQaddress= write_byte[15];
  int address_val = write_byte[IQaddress];
    chipselect(0,arraynum[Unitsel1]);
    LTC5599_write_read(LTC5599_CS, address[IQaddress], rw, address_val, &readback_byte);
    delay(I2CupdateSpeed);
    chipCSBclose();
    Serial.println(arraynum[Unitsel1]);
    delay(I2CupdateSpeed);
  Serial.println("---IQstart /n");
  Serial.println("ADDRESS and val: /n");
  Serial.println(address[IQaddress]);
  Serial.println(address_val);
  Serial.println("---IQEnd /n");


}



//-----------------------------------SPI for DAC Update ------------------------------
void DACUpdate(){
  int Unitsel = write_byte[0];
  int Unitsell = arraynum[Unitsel] + 8;
  
  Serial.println(Unitsel);
  Serial.println("\n");
  //-------------------DAC update----------------
   uint8_t CMDAddI = write_byte[12];
   IValu.Valbyte[0]= write_byte[14];
   IValu.Valbyte[1]= write_byte[13];
   uint8_t CMDAddQ = write_byte[9];
   QValu.Valbyte[0]= write_byte[11];
   QValu.Valbyte[1]= write_byte[10];

  uint16_t AmpbitI = IValu.fullword;
  uint16_t AmpbitQ = QValu.fullword;
  
  //-------------------DAC update----------------
  //----I
  chipselect(0,Unitsell);
  SPI.beginTransaction(SPISettings(2000000, MSBFIRST, SPI_MODE1));
  SPI.transfer(CMDAddI); // first byte
  SPI.transfer16(AmpbitI); // second byte
  SPI.endTransaction();
  delay(I2CupdateSpeed);
  chipCSBclose();
 
  delay(I2CupdateSpeed);
  //----Q
  chipselect(0,Unitsell);
  SPI.beginTransaction(SPISettings(2000000, MSBFIRST, SPI_MODE1));
  SPI.transfer(CMDAddQ); // first byte
  SPI.transfer16(AmpbitQ); // second byte
  SPI.endTransaction();
  delay(I2CupdateSpeed);
  chipCSBclose();
  Serial.println(CMDAddI);
  Serial.println(IValu.Valbyte[0]);
  Serial.println(IValu.Valbyte[1]);
  Serial.println(IValu.fullword);
  Serial.println(CMDAddQ);
  Serial.println(QValu.Valbyte[0]);
  Serial.println(QValu.Valbyte[1]);
  Serial.println(QValu.fullword);

  Serial.println("---DACEnd /n");
}

// void initial setting function

void initset(int ii){

   Serial.println("Unitcell update");
    Serial.println(ii);
     Serial.println("\n");
  //-----------------------------------------------initial setting start
      // //---------------------LTC5589 Setting initialise 
      //   Serial.println("Phase shift started");

        for (int i = 0; i <= 8; i++) {

        // digitalWrite(8, LOW);
          Serial.println("address");
          Serial.println(address[i]);
          chipselect(0,arraynum[ii]);
          delay(SPIupdateSpeed);
          LTC5599_write_read(LTC5599_CS, address[i], rw, write_byted_init0[i], &readback_byte); //LTC5599_CS, address[i], rw, write_byted_init0[i], &readback_byte); 
          chipCSBclose();
       
          delay(SPIupdateSpeed);
        };

        
      //   Serial.println("modulator initialized");
      //-------------------------DAC initialise 
      //------------Q Value;
      chipselect(0,arraynum[ii]+8);
      SPI.beginTransaction(SPISettings(2000000, MSBFIRST, SPI_MODE1));
      SPI.transfer(49); // first byte
      SPI.transfer16(32767); // second byte
      delay(SPIupdateSpeed);
      SPI.endTransaction();
      chipCSBclose(); 
      Serial.println("DAC update (CSB,address,Value)");
      delay(SPIupdateSpeed);

      //------------I Value;
      chipselect(0,arraynum[ii]+8);
      SPI.beginTransaction(SPISettings(2000000, MSBFIRST, SPI_MODE1));
      SPI.transfer(56); // first byte
      SPI.transfer16(61166); // second byte
      delay(SPIupdateSpeed); 
      SPI.endTransaction();
      chipCSBclose(); //Q register 
      Serial.println("DAC update (CSB,address,Value)");
      delay(SPIupdateSpeed); 

      Serial.println("DAC initialized");
       Serial.println("\n");

}
