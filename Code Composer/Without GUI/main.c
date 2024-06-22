#include <msp430.h>
#include <stdbool.h>
#include <stdint.h>
#include "I2CController.h"
#include "FSCVMotherBoardV2.h"


#define SLAVE_ADDR1 0x74
#define SLAVE_ADDR2 0x76 // Address of the I2C slave device

void initIOExpander(unsigned int slave_addr, unsigned int PORT0, unsigned int PORT1);
void initFSCVMotherboard();

extern uint8_t MCU_PORT7;
extern uint8_t MCU_PORT4;
extern uint8_t MCU_PORT3;
extern uint8_t MCU_PORT6;
extern uint8_t IOE1_PORT0;
extern uint8_t IOE1_PORT1;
extern uint8_t IOE2_PORT0;
extern uint8_t IOE2_PORT1;


void main(void) {
    WDTCTL = WDTPW | WDTHOLD; // Stop watchdog timer


    //For interrupt and reset
    P2DIR &= ~BIT7;
    P2DIR |= BIT6;
    P2OUT |= BIT6;
    P5DIR &= ~BIT1;
    P5DIR |= BIT0;
    P5OUT |= BIT0;


    initFSCVMotherboard();

    init_CLK();
    init_I2C();
    initIOExpander(SLAVE_ADDR1,~IOE1_PORT0,~IOE1_PORT1);
    initIOExpander(SLAVE_ADDR2,~IOE2_PORT0,~IOE2_PORT1);

    P7DIR |= 0xff;
    P4DIR |= 0xff;
    P3DIR |= 0xff;
    P6DIR |= 0xff;

    P7OUT = ~MCU_PORT7;
    P4OUT = ~MCU_PORT4;
    P3OUT = ~MCU_PORT3;
    P6OUT = ~MCU_PORT6;


}

void initIOExpander(unsigned int slave_addr, unsigned int Port0, unsigned int Port1){
    write_I2C_byte(slave_addr, 0x06, 0x00);
    write_I2C_byte(slave_addr, 0x07, 0x00);
    write_I2C_byte(slave_addr, 0x02, Port0);
    write_I2C_byte(slave_addr, 0x03, Port1);
}




void initFSCVMotherboard(){
    enableVDD(CH_12);
    enableVDD(CH_34);
    enableVDD(CH_56);
    enableVDD(CH_78);
    enableVDD(CH_DE);

//    enableIREF(CH_12);
//    enableIREFTEST(CH_12);

//    enableIREF(CH_34);
//    enableIREFTEST(CH_34);
//
//    enableIREF(CH_56);
//    enableIREFTEST(CH_56);
//
//    enableIREF(CH_78);
//    enableIREFTEST(CH_78);
//
//    enableIREF(CH_DE);
//    enableIREFTEST(CH_DE);

    //void chXSel (ChannelEnum ch, bool conditioningEn, bool HPFEn);
        //A = 1,5
        //B = 2,6
        //C = 3,7
        //D = 4,8
    //Write your code here
//    chDE(false,true,false);
   chASel (CH_1, false,false,false);
//   chBSel (CH_2, false,false,false);
//   chCSel (CH_3, false,false,false);
//   chDSel (CH_4, false,false,false);
}

