#include <msp430.h>
#include "I2CController.h"
#define SLAVE_ADDR1 0x74
#define SLAVE_ADDR2 0x76 // Address of the I2C slave device
// Function to initialize the I2C
void initI2C(void) {
    // Implementation for initializing I2C
    UCB0CTLW0 |= UCSWRST;

    UCB0CTLW0 |= UCMODE_3; // Choose I2C Mode
    UCB0CTLW0 |= UCMST;
    UCB0CTLW0 |= UCSYNC;
    UCB0CTLW0 |= UCSSEL__SMCLK;
    UCB0CTLW0 |= UCTR;
    UCB0CTLW1 |= UCASTP_2;
    UCB0BRW = 80;
    UCB0TBCNT = 0x02;
//    UCB0I2CSA = SLAVE_ADDR1;
    //enabling 5.2, 5.3 as I2C pins for MSP430FR4132
    P5SEL0 |= BIT2;
    P5SEL0 |= BIT3;
    UCB0CTLW0 &= ~UCSWRST;


    __delay_cycles(3000);
}

// Function to write byte via I2C
void writeI2CByte(unsigned int slave_addr, unsigned int reg_addr, unsigned int data) {
    while (UCB0STAT & UCBBUSY); // Wait until I2C bus is not busy

    UCB0I2CSA = slave_addr; // Set slave address
    UCB0CTLW0 |= UCTR + UCTXSTT; // Set as transmitter and generate start condition

    while (!(UCB0IFG & UCTXIFG0)); // Wait until TX buffer is ready
    UCB0TXBUF = reg_addr; // Send register address

    while (!(UCB0IFG & UCTXIFG0)); // Wait until TX buffer is ready
    UCB0TXBUF = data; // Send data
}
