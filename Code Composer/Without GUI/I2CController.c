#include <msp430.h>
#include "I2CController.h"
#define SLAVE_ADDR1 0x74
// Function to initialize the clock
void init_CLK(void) {
    __bis_SR_register(SCG0); // disable FLL

    // Initialize Clock System
    // SMCLK = MCLK = DCO + FLL + 32KHz REFO REF = 1MHz
    CSCTL3 |= SELREF__REFOCLK; // Set REFO as FLL reference source
    CSCTL1 = DCOFTRIMEN | DCOFTRIM0 | DCOFTRIM1 | DCORSEL_0; // DCOFTRIM=3, DCO Range = 1MHz
    CSCTL2 = FLLD_0 + 30; // DCODIV = 1MHz
    __delay_cycles(3);
    __bic_SR_register(SCG0); // enable FLL

    CSCTL4 = SELMS__DCOCLKDIV | SELA__REFOCLK; // set default REFO(~32768Hz) as ACLK source, ACLK = 32768Hz
    // default DCODIV as MCLK and SMCLK source
}

// Function to initialize the I2C
void init_I2C(void) {
    // Implementation for initializing I2C
    UCB0CTLW0 |= UCSWRST;

    UCB0CTLW0 |= UCMODE_3; // Choose I2C Mode
    UCB0CTLW0 |= UCMST;
    UCB0CTLW0 |= UCSYNC;
    UCB0CTLW0 |= UCSSEL_3;
    UCB0CTLW0 |= UCTR;
    UCB0CTLW1 |= UCASTP_2;
    UCB0BRW = 10;
    UCB0TBCNT = 0x02;
//    UCB0I2CSA = SLAVE_ADDR1;
    //enabling 5.2, 5.3 as I2C pins for MSP430FR4132
    P5SEL0 |= BIT2;
    P5SEL0 |= BIT3;
    PM5CTL0 &= ~LOCKLPM5;
    UCB0CTLW0 &= ~UCSWRST;


    __delay_cycles(3000);
}

// Function to write byte via I2C
void write_I2C_byte(unsigned int slave_addr, unsigned int reg_addr, unsigned int data) {
    while (UCB0STAT & UCBBUSY); // Wait until I2C bus is not busy

    UCB0I2CSA = slave_addr; // Set slave address
    UCB0CTLW0 |= UCTR + UCTXSTT; // Set as transmitter and generate start condition

    while (!(UCB0IFG & UCTXIFG0)); // Wait until TX buffer is ready
    UCB0TXBUF = reg_addr; // Send register address

    while (!(UCB0IFG & UCTXIFG0)); // Wait until TX buffer is ready
    UCB0TXBUF = data; // Send data
}
