#include<msp430.h>

#include "UARTController.h"
#ifndef UARTCONTROLLER_C_
#define UARTCONTROLLER_C_

void initUART(){
    // Configure UART pins
    P1SEL0 |= BIT0 | BIT1;// set P1.0 and P1.1 as UART pin as second function

    // Configure UART
    UCA0CTLW0 |= UCSWRST;
    UCA0CTLW0 |= UCSSEL__SMCLK;

    // Baud Rate calculation
    // 8000000/(16*9600) = 52.083
    // Fractional portion = 0.083
    // User's Guide Table 14-4: UCBRSx = 0x49
    // UCBRFx = int ( (52.083-52)*16) = 1
    UCA0BR0 = 52;                             // 8000000/16/9600
    UCA0BR1 = 0x00;
    UCA0MCTLW = 0x4900 | UCOS16 | UCBRF_1;

    UCA0CTLW0 &= ~UCSWRST;                    // Initialize eUSCI
    UCA0IE |= UCRXIE;                         // Enable USCI_A0 RX interrupt

    __bis_SR_register(LPM3_bits|GIE);         // Enter LPM3, interrupts enabled
    __no_operation();                         // For debugger
}


#endif /* UARTCONTROLLER_C_ */
