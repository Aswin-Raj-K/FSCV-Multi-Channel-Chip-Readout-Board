
#ifndef FSCVMOTHERBOARDV2_H_
#define FSCVMOTHERBOARDV2_H_

#include <msp430.h>
#include <stdbool.h>

typedef enum {
    CH_1 = 1,
    CH_2 = 2,
    CH_3 = 3,
    CH_4 = 4,
    CH_5 = 5,
    CH_6 = 6,
    CH_7 = 7,
    CH_8 = 8,
    CH_12 = 12,
    CH_34 = 34,
    CH_56 = 56,
    CH_78 = 78,
    CH_DE = 0
} ChannelEnum;


//MCU Pins

//Port 7
#define IREF_EN_12 BIT5
#define IREF_EN_78 BIT4
#define CH_B BIT3
#define CH_D BIT2
#define CH_CD_COND BIT1
#define CH_AB_COND BIT0

//Port 4
#define CH_C BIT7
#define CH_A BIT6
#define CH_AB BIT5
#define CH_CD BIT4

//Port 3
#define IREF_TEST_12 BIT0
#define EN_78 BIT1
#define CH_EN_2 BIT2
#define COND_EN_5 BIT3
#define HP_BYPASS_EN_2 BIT4
#define COND_EN_2 BIT5
#define COND_EN_6 BIT6
#define HP_BYPASS_EN_6 BIT7

//Port 6
#define COND_EN_1 BIT0
#define CH_EN_6 BIT1
#define HP_BYPASS_EN_1 BIT2
#define CH_EN_1 BIT3
#define IREF_TEST_78 BIT4

//IO Expander 1
#define IOEXPANDER1_ADDR 0x74
//Port 0
#define CH_EN_D BIT0
#define CH_EN_8 BIT1
#define HP_BYPASS_EN_8 BIT2
#define COND_EN_8 BIT3
#define COND_EN_7 BIT4
#define HP_BYPASS_EN_7 BIT5
#define CH_EN_7 BIT6
#define EN_12 BIT7

//Port 1
#define HP_BYPASS_EN_D BIT0
#define IREF_TEST_D BIT1
#define EN_D BIT2
#define IREF_EN_D BIT3
#define COND_EN_D BIT4
#define IREF_EN_56 BIT5
#define IREF_TEST_56 BIT6
#define T_VRPS_D BIT7


//IO Expander 2
#define IOEXPANDER2_ADDR 0x76
//Port 0
#define CH_EN_4 BIT0
#define IREF_SWITCH_PR BIT1
#define SEL1_PR BIT2
#define SEL2_PR BIT3
#define SEL3_PR BIT4
#define HP_BYPASS_EN_5 BIT5
#define CH_EN_5 BIT6
#define EN_56 BIT7

//Port 1
#define IREF_TEST_34 BIT0
#define IREF_EN_34 BIT1
#define EN_34 BIT2
#define CH_EN_3 BIT3
#define HP_BYPASS_EN_3 BIT4
#define COND_EN_3 BIT5
#define COND_EN_4 BIT6
#define HP_BYPASS_EN_4 BIT7


//Functions
void enableChannel(ChannelEnum channelEn);
void enableVDD(ChannelEnum channelEn);
void enableIREFTEST(ChannelEnum channelEn);
void enableIREF(ChannelEnum channelEn);
void enableHPF(ChannelEnum channelEn);
void enableConditioning(ChannelEnum channelEn);
void chASel(ChannelEnum ch, bool conditioningEn, bool HPFEn, bool irefTestEn);
void chBSel(ChannelEnum ch, bool conditioningEn, bool HPFEn, bool irefTestEn);
void chCSel(ChannelEnum ch, bool conditioningEn, bool HPFEn, bool irefTestEn);
void chDSel(ChannelEnum ch, bool conditioningEn, bool HPFEn, bool irefTestEn);
void chDE(bool conditioningEn, bool HPFEn, bool irefTestEn);

void initChannel(ChannelEnum ch);

#endif /* FSCVMOTHERBOARDV2_H_ */
