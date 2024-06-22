#include <msp430.h>
#include "ClkSetup.h"
#include "I2CController.h"
#include "UARTController.h"
#include <stdint.h>

void initGPIO();
void setGPIO(char []);
void initIOExpander(unsigned int slave_addr, unsigned int Port0, unsigned int Port1);

uint8_t IOE1_PORT0;
uint8_t IOE1_PORT1;
uint8_t IOE2_PORT0;
uint8_t IOE2_PORT1;


#define SLAVE_ADDR1 0x74
#define SLAVE_ADDR2 0x76

char RXbuffer[32];
const unsigned char maxRXbytes = sizeof(RXbuffer);
unsigned int RXbytes = 0;

const char message[] = "SUCCESS\n";
const unsigned char messageLength = sizeof(message)-1;
unsigned char TXbytes = 0;


int main(void)
{
  WDTCTL = WDTPW | WDTHOLD;                // Stop watchdog timer

  // Configure GPIO
  initGPIO();
  PM5CTL0 &= ~LOCKLPM5;                    // Disable the GPIO power-on default high-impedance mode
  initClk();
  initI2C();
  initUART();

  initIOExpander(SLAVE_ADDR1, ~0xa4, ~0x05);
  initIOExpander(SLAVE_ADDR2, ~0xa0, ~0x94);
}

#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector=USCI_A0_VECTOR
__interrupt void USCI_A0_ISR(void)
#elif defined(__GNUC__)
void __attribute__ ((interrupt(USCI_A0_VECTOR))) USCI_A0_ISR (void)
#else
#error Compiler not supported!
#endif
{
    switch(__even_in_range(UCA0IV,USCI_UART_UCTXCPTIFG))
           {
             case USCI_NONE: break;
             case USCI_UART_UCRXIFG:

                 if(RXbytes < maxRXbytes)
                 {
                     // Get the byte
                     RXbuffer[RXbytes] = UCA0RXBUF;
                     if((RXbytes == 0) && (RXbuffer[0]=='T')){
                             UCA0IE |= UCTXIE;
                             RXbytes = 0;
                     }
                     else if(RXbytes == 8)
                     {
                         // Start message transmission
                         UCA0IE |= UCTXIE;
                         P3OUT = ~RXbuffer[1];
                         P4OUT = ~RXbuffer[2];
                         P6OUT = ~RXbuffer[3];
                         P7OUT = ~RXbuffer[4];
                         IOE1_PORT0 = ~RXbuffer[5];
                         IOE1_PORT1 = ~RXbuffer[6];
                         IOE2_PORT0 = ~RXbuffer[7];
                         IOE2_PORT1 = ~RXbuffer[8];

                         initIOExpander(SLAVE_ADDR1, IOE1_PORT0, IOE1_PORT1);
                         initIOExpander(SLAVE_ADDR2, IOE2_PORT0, IOE2_PORT1);

                         RXbytes = 0;
                     }
                     else
                         RXbytes++;

                 }
                 break;

             case USCI_UART_UCTXIFG:

                 // Transmit the byte
                 UCA0TXBUF = message[TXbytes++];

                 // If last byte sent, disable the interrupt
                 if(TXbytes == messageLength)
                 {
                     UCA0IE &= ~UCTXIE;
                     TXbytes = 0;
                 }
                 break;

             case USCI_UART_UCSTTIFG: break;
             case USCI_UART_UCTXCPTIFG: break;
             default: break;
           }
}



void initIOExpander(unsigned int slave_addr, unsigned int Port0, unsigned int Port1){
    writeI2CByte(slave_addr, 0x06, 0x00);
    writeI2CByte(slave_addr, 0x07, 0x00);
    writeI2CByte(slave_addr, 0x02, Port0);
    writeI2CByte(slave_addr, 0x03, Port1);
}

void initGPIO()
{
    P7DIR |= 0xff;
    P4DIR |= 0xff;
    P3DIR |= 0x92;
    P6DIR |= 0x04;
}

