#include "FSCVMotherBoardV2.h"
#include <stdint.h>

uint8_t MCU_PORT7 = 0x00;
uint8_t MCU_PORT4 = 0x00;
uint8_t MCU_PORT3 = 0x00 | HP_BYPASS_EN_2 | HP_BYPASS_EN_6;
uint8_t MCU_PORT6 = 0x00 | HP_BYPASS_EN_1;
uint8_t IOE1_PORT0 = 0x00 | HP_BYPASS_EN_7 | HP_BYPASS_EN_8;
uint8_t IOE1_PORT1 = 0x00 | HP_BYPASS_EN_D;
uint8_t IOE2_PORT0 = 0x00 | HP_BYPASS_EN_5;
uint8_t IOE2_PORT1 = 0x00 | HP_BYPASS_EN_3 | HP_BYPASS_EN_4;


void enableChannel(ChannelEnum channelEn) {

    switch (channelEn) {
        case CH_1:
            MCU_PORT6 |= CH_EN_1;
            break;
        case CH_2:
            MCU_PORT3 |= CH_EN_2;
            break;
        case CH_3:
            IOE2_PORT1 |= CH_EN_3;
            break;
        case CH_4:
            IOE2_PORT0 |= CH_EN_4;
            break;
        case CH_5:
            IOE2_PORT0 |= CH_EN_5;
            break;
        case CH_6:
            MCU_PORT6 |= CH_EN_6;
            break;
        case CH_7:
            IOE1_PORT0 |= CH_EN_7;
            break;
        case CH_8:
            IOE1_PORT0 |= CH_EN_8;
            break;
        case CH_DE:
            IOE1_PORT0 |= CH_EN_D;
            break;
    }
}

void enableVDD(ChannelEnum channelEn){
    switch (channelEn) {
            case CH_12:
            case CH_1:
            case CH_2:
                IOE1_PORT0 |= EN_12;
                break;
            case CH_34:
            case CH_3:
            case CH_4:
                IOE2_PORT1 |= EN_34;
                break;
            case CH_56:
            case CH_5:
            case CH_6:
                IOE2_PORT0 |= EN_56;
                break;
            case CH_78:
            case CH_7:
            case CH_8:
                MCU_PORT3 |= EN_78;
                break;
            case CH_DE:
                IOE1_PORT1 |= EN_D;
                break;
        }
}


void enableIREF(ChannelEnum channelEn){
    switch (channelEn) {
            case CH_12:
            case CH_1:
            case CH_2:
                MCU_PORT7 |= IREF_EN_12;
                break;
            case CH_34:
            case CH_3:
            case CH_4:
                IOE2_PORT1 |= IREF_EN_34;
                break;
            case CH_56:
            case CH_5:
            case CH_6:
                IOE1_PORT1 |= IREF_EN_56;
                break;
            case CH_78:
            case CH_7:
            case CH_8:
                MCU_PORT7 |= IREF_EN_78;
                break;
            case CH_DE:
                IOE1_PORT1 |= IREF_EN_D;
                break;
        }
}

void enableIREFTEST(ChannelEnum channelEn){
    switch (channelEn) {
            case CH_12:
            case CH_1:
            case CH_2:
                MCU_PORT3 |= IREF_TEST_12;
                break;
            case CH_34:
            case CH_3:
            case CH_4:
                IOE2_PORT1 |= IREF_TEST_34;
                break;
            case CH_56:
            case CH_5:
            case CH_6:
                IOE1_PORT1 |= IREF_TEST_56;
                break;
            case CH_78:
            case CH_7:
            case CH_8:
                MCU_PORT6 |= IREF_TEST_78;
                break;
            case CH_DE:
                IOE1_PORT1 |= IREF_TEST_D;
                break;
        }
}

void enableHPF(ChannelEnum channelEn) {

    switch (channelEn) {
        case CH_1:
            MCU_PORT6 &= ~HP_BYPASS_EN_1;
            break;
        case CH_2:
            MCU_PORT3 &= ~HP_BYPASS_EN_2;
            break;
        case CH_3:
            IOE2_PORT1 &= ~HP_BYPASS_EN_3;
            break;
        case CH_4:
            IOE2_PORT1 &= ~HP_BYPASS_EN_4;
            break;
        case CH_5:
            IOE2_PORT0 &= ~HP_BYPASS_EN_5;
            break;
        case CH_6:
            MCU_PORT3 &= ~HP_BYPASS_EN_6;
            break;
        case CH_7:
            IOE1_PORT0 &= ~HP_BYPASS_EN_7;
            break;
        case CH_8:
            IOE1_PORT0 &= ~HP_BYPASS_EN_8;
            break;
        case CH_DE:
            IOE1_PORT1 &= ~HP_BYPASS_EN_D;
            break;
    }
}

void enableConditioning(ChannelEnum channelEn) {

    switch (channelEn) {
        case CH_1:
            MCU_PORT6 |= COND_EN_1;
            break;
        case CH_2:
            MCU_PORT3 |= COND_EN_2;
            break;
        case CH_3:
            IOE2_PORT1 |= COND_EN_3;
            break;
        case CH_4:
            IOE2_PORT1 |= COND_EN_4;
            break;
        case CH_5:
            MCU_PORT3 |= COND_EN_5;
            break;
        case CH_6:
            MCU_PORT3 |= COND_EN_6;
            break;
        case CH_7:
            IOE1_PORT0 |= COND_EN_7;
            break;
        case CH_8:
            IOE1_PORT0 |= COND_EN_8;
            break;
        case CH_DE:
            IOE1_PORT1 |= COND_EN_D;
            break;
    }
}


void chASel (ChannelEnum ch, bool conditioningEn, bool HPFEn, bool irefTestEn){
    if(ch == CH_1 || ch == CH_5){
        initChannel(ch);
        if(conditioningEn){
            enableConditioning(ch);
            MCU_PORT7 |= CH_AB_COND;
        }
        if(HPFEn)
            enableHPF(ch);
        if(irefTestEn)
            enableIREFTEST(ch);

        if(ch == CH_5){
            MCU_PORT4 |= CH_A;
            MCU_PORT4 |= CH_AB;
        }
    }
}

void chBSel (ChannelEnum ch, bool conditioningEn, bool HPFEn, bool irefTestEn){
    if(ch == CH_2 || ch == CH_6){
        initChannel(ch);
        if(conditioningEn){
            enableConditioning(ch);
            MCU_PORT7 |= CH_AB_COND;
        }
        if(HPFEn)
            enableHPF(ch);
        if(irefTestEn)
            enableIREFTEST(ch);
        if(ch == CH_6){
            MCU_PORT7 |= CH_B;
            MCU_PORT4 |= CH_AB;
        }
    }
}

void chCSel (ChannelEnum ch, bool conditioningEn, bool HPFEn, bool irefTestEn){
    if(ch == CH_3|| ch == CH_7){
        initChannel(ch);
        if(conditioningEn){
            enableConditioning(ch);
            MCU_PORT7 |= CH_CD_COND;
        }
        if(HPFEn)
            enableHPF(ch);
        if(irefTestEn)
            enableIREFTEST(ch);
        if(ch == CH_7){
            MCU_PORT4 |= CH_C;
            MCU_PORT4 |= CH_CD;
        }
    }
}

void chDSel (ChannelEnum ch, bool conditioningEn, bool HPFEn, bool irefTestEn){
    if(ch == CH_4|| ch == CH_8){
            initChannel(ch);
            if(conditioningEn){
                enableConditioning(ch);
                MCU_PORT7 |= CH_CD_COND;
            }
            if(HPFEn)
                enableHPF(ch);
            if(irefTestEn)
                enableIREFTEST(ch);
            if(ch == CH_8){
                MCU_PORT7 |= CH_D;
                MCU_PORT4 |= CH_CD;
            }
        }
}

void chDE(bool conditioningEn, bool HPFEn, bool irefTestEn){
    initChannel(CH_DE);
    if(conditioningEn){
        enableConditioning(CH_DE);
        IOE1_PORT1 |= T_VRPS_D;
    }
    if(HPFEn)
        enableHPF(CH_DE);
    if(irefTestEn)
        enableIREFTEST(CH_DE);
}

void initChannel(ChannelEnum ch){
    enableChannel(ch);
    enableIREF(ch);
}



