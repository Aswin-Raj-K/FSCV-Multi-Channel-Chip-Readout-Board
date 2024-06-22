from main import Channel, CurrentGeneration, PR


class FSCVMotherboard:

	# MCU Pins

	# Port 7
	IREF_EN_12 = 1 << 5
	IREF_EN_78 = 1 << 4
	CH_B = 1 << 3
	CH_D = 1 << 2
	CH_CD_COND = 1 << 1
	CH_AB_COND = 1 << 0

	# Port 4
	CH_C = 1 << 7
	CH_A = 1 << 6
	CH_AB = 1 << 5
	CH_CD = 1 << 4

	# Port 3
	IREF_TEST_12 = 1 << 0
	EN_78 = 1 << 1
	CH_EN_2 = 1 << 2
	COND_EN_5 = 1 << 3
	HP_BYPASS_EN_2 = 1 << 4
	COND_EN_2 = 1 << 5
	COND_EN_6 = 1 << 6
	HP_BYPASS_EN_6 = 1 << 7

	# Port 6
	COND_EN_1 = 1 << 0
	CH_EN_6 = 1 << 1
	HP_BYPASS_EN_1 = 1 << 2
	CH_EN_1 = 1 << 3
	IREF_TEST_78 = 1 << 4

	# IO Expander 1
	IOEXPANDER1_ADDR = 0x74
	# Port 0
	CH_EN_D = 1 << 0
	CH_EN_8 = 1 << 1
	HP_BYPASS_EN_8 = 1 << 2
	COND_EN_8 = 1 << 3
	COND_EN_7 = 1 << 4
	HP_BYPASS_EN_7 = 1 << 5
	CH_EN_7 = 1 << 6
	EN_12 = 1 << 7

	# Port 1
	HP_BYPASS_EN_D = 1 << 0
	IREF_TEST_D = 1 << 1
	EN_D = 1 << 2
	IREF_EN_D = 1 << 3
	COND_EN_D = 1 << 4
	IREF_EN_56 = 1 << 5
	IREF_TEST_56 = 1 << 6
	T_VRPS_D = 1 << 7

	# IO Expander 2
	IOEXPANDER2_ADDR = 0x76
	# Port 0
	CH_EN_4 = 1 << 0
	IREF_SWITCH_PR = 1 << 1
	SEL1_PR = 1 << 2
	SEL2_PR = 1 << 3
	SEL3_PR = 1 << 4
	HP_BYPASS_EN_5 = 1 << 5
	CH_EN_5 = 1 << 6
	EN_56 = 1 << 7

	# Port 1
	IREF_TEST_34 = 1 << 0
	IREF_EN_34 = 1 << 1
	EN_34 = 1 << 2
	CH_EN_3 = 1 << 3
	HP_BYPASS_EN_3 = 1 << 4
	COND_EN_3 = 1 << 5
	COND_EN_4 = 1 << 6
	HP_BYPASS_EN_4 = 1 << 7

	CH_1 = 1
	CH_2 = 2
	CH_3 = 3
	CH_4 = 4
	CH_5 = 5
	CH_6 = 6
	CH_7 = 7
	CH_8 = 8
	CH_DE = 9
	CH_12 = 12
	CH_34 = 34
	CH_56 = 56
	CH_78 = 78

	MCU_PORT7 = "MCU_PORT7"
	MCU_PORT4 = "MCU_PORT4"
	MCU_PORT3 = "MCU_PORT3"
	MCU_PORT6 = "MCU_PORT6"
	IOE1_PORT0 = "IOE1_PORT0"
	IOE1_PORT1 = "IOE1_PORT1"
	IOE2_PORT0 = "IOE2_PORT0"
	IOE2_PORT1 = "IOE2_PORT1"

	def __init__(self):
		self.values = {
			FSCVMotherboard.MCU_PORT7: 0x00,
			FSCVMotherboard.MCU_PORT4: 0x00,
			FSCVMotherboard.MCU_PORT3: 0x00 | FSCVMotherboard.HP_BYPASS_EN_2 | FSCVMotherboard.HP_BYPASS_EN_6 | FSCVMotherboard.EN_78,
			FSCVMotherboard.MCU_PORT6: 0x00 | FSCVMotherboard.HP_BYPASS_EN_1,
			FSCVMotherboard.IOE1_PORT0: 0x00 | FSCVMotherboard.HP_BYPASS_EN_7 | FSCVMotherboard.HP_BYPASS_EN_8 | FSCVMotherboard.EN_12,
			FSCVMotherboard.IOE1_PORT1: 0x00 | FSCVMotherboard.HP_BYPASS_EN_D | FSCVMotherboard.EN_D,
			FSCVMotherboard.IOE2_PORT0: 0x00 | FSCVMotherboard.HP_BYPASS_EN_5 | FSCVMotherboard.EN_56,
			FSCVMotherboard.IOE2_PORT1: 0x00 | FSCVMotherboard.HP_BYPASS_EN_3 | FSCVMotherboard.HP_BYPASS_EN_4 | FSCVMotherboard.EN_34
		}

	def initChannel(self, channelName, data):
		if (channelName == 'A'):
			self.channelA(data)
		elif (channelName == 'B'):
			self.channelB(data)
		elif (channelName == 'C'):
			self.channelC(data)
		elif (channelName == 'D'):
			self.channelD(data)
		else:
			self.initDebugChannel(data)

	def getValues(self):
		return self.values

	def initDebugChannel(self, data):
		if data[Channel.CH_EN]:
			self.enableChannel(FSCVMotherboard.CH_DE)

		if data[Channel.COND_EN]:
			self.enableConditioning(FSCVMotherboard.CH_DE)
			self.values[FSCVMotherboard.IOE1_PORT1] |= FSCVMotherboard.T_VRPS_D

		if data[Channel.HPF_EN]:
			self.enableHPF(FSCVMotherboard.CH_DE)

	def channelA(self, data):

		if data[Channel.CH_EN]:
			self.enableChannel(data[Channel.SEL_CH])

		if data[Channel.COND_EN]:
			self.enableConditioning(data[Channel.SEL_CH])
			self.values[FSCVMotherboard.MCU_PORT7] |= FSCVMotherboard.CH_AB_COND

		if data[Channel.HPF_EN]:
			self.enableHPF(data[Channel.SEL_CH])


		if data[Channel.SEL_CH] == FSCVMotherboard.CH_5:
			self.values[FSCVMotherboard.MCU_PORT4] |= FSCVMotherboard.CH_A
			self.values[FSCVMotherboard.MCU_PORT4] |= FSCVMotherboard.CH_AB

	def channelB(self, data):

		if data[Channel.CH_EN]:
			self.enableChannel(data[Channel.SEL_CH])

		if data[Channel.COND_EN]:
			self.enableConditioning(data[Channel.SEL_CH])
			self.values[FSCVMotherboard.MCU_PORT7] |= FSCVMotherboard.CH_AB_COND

		if data[Channel.HPF_EN]:
			self.enableHPF(data[Channel.SEL_CH])

		if data[Channel.SEL_CH] == FSCVMotherboard.CH_6:
			self.values[FSCVMotherboard.MCU_PORT7] |= FSCVMotherboard.CH_B
			self.values[FSCVMotherboard.MCU_PORT4] |= FSCVMotherboard.CH_AB

	def channelC(self, data):

		if data[Channel.CH_EN]:
			self.enableChannel(data[Channel.SEL_CH])

		if data[Channel.COND_EN]:
			self.enableConditioning(data[Channel.SEL_CH])
			self.values[FSCVMotherboard.MCU_PORT7] |= FSCVMotherboard.CH_CD_COND

		if data[Channel.HPF_EN]:
			self.enableHPF(data[Channel.SEL_CH])


		if data[Channel.SEL_CH] == FSCVMotherboard.CH_7:
			self.values[FSCVMotherboard.MCU_PORT4] |= FSCVMotherboard.CH_C
			self.values[FSCVMotherboard.MCU_PORT4] |= FSCVMotherboard.CH_CD

	def channelD(self, data):
		if data[Channel.CH_EN]:
			self.enableChannel(data[Channel.SEL_CH])

		if data[Channel.COND_EN]:
			self.enableConditioning(data[Channel.SEL_CH])
			self.values[FSCVMotherboard.MCU_PORT7] |= FSCVMotherboard.CH_CD_COND

		if data[Channel.HPF_EN]:
			self.enableHPF(data[Channel.SEL_CH])

		if data[Channel.SEL_CH] == FSCVMotherboard.CH_8:
			self.values[FSCVMotherboard.MCU_PORT7] |= FSCVMotherboard.CH_D
			self.values[FSCVMotherboard.MCU_PORT4] |= FSCVMotherboard.CH_CD

	def enableHPF(self, channelEn):
		switcher = {
			FSCVMotherboard.CH_1: (FSCVMotherboard.MCU_PORT6, ~FSCVMotherboard.HP_BYPASS_EN_1),
			FSCVMotherboard.CH_2: (FSCVMotherboard.MCU_PORT3, ~FSCVMotherboard.HP_BYPASS_EN_2),
			FSCVMotherboard.CH_3: (FSCVMotherboard.IOE2_PORT1, ~FSCVMotherboard.HP_BYPASS_EN_3),
			FSCVMotherboard.CH_4: (FSCVMotherboard.IOE2_PORT1, ~FSCVMotherboard.HP_BYPASS_EN_4),
			FSCVMotherboard.CH_5: (FSCVMotherboard.IOE2_PORT0, ~FSCVMotherboard.HP_BYPASS_EN_5),
			FSCVMotherboard.CH_6: (FSCVMotherboard.MCU_PORT3, ~FSCVMotherboard.HP_BYPASS_EN_6),
			FSCVMotherboard.CH_7: (FSCVMotherboard.IOE1_PORT0, ~FSCVMotherboard.HP_BYPASS_EN_7),
			FSCVMotherboard.CH_8: (FSCVMotherboard.IOE1_PORT0, ~FSCVMotherboard.HP_BYPASS_EN_8),
			FSCVMotherboard.CH_DE: (FSCVMotherboard.IOE1_PORT1, ~FSCVMotherboard.HP_BYPASS_EN_D),
		}
		port, mask = switcher.get(channelEn, (None, None))
		if port is not None and mask is not None:
			self.values[port] &= mask

	def enableConditioning(self, channelEn):
		switcher = {
			FSCVMotherboard.CH_1: (FSCVMotherboard.MCU_PORT6, FSCVMotherboard.COND_EN_1),
			FSCVMotherboard.CH_2: (FSCVMotherboard.MCU_PORT3, FSCVMotherboard.COND_EN_2),
			FSCVMotherboard.CH_3: (FSCVMotherboard.IOE2_PORT1, FSCVMotherboard.COND_EN_3),
			FSCVMotherboard.CH_4: (FSCVMotherboard.IOE2_PORT1, FSCVMotherboard.COND_EN_4),
			FSCVMotherboard.CH_5: (FSCVMotherboard.MCU_PORT3, FSCVMotherboard.COND_EN_5),
			FSCVMotherboard.CH_6: (FSCVMotherboard.MCU_PORT3, FSCVMotherboard.COND_EN_6),
			FSCVMotherboard.CH_7: (FSCVMotherboard.IOE1_PORT0, FSCVMotherboard.COND_EN_7),
			FSCVMotherboard.CH_8: (FSCVMotherboard.IOE1_PORT0, FSCVMotherboard.COND_EN_8),
			FSCVMotherboard.CH_DE: (FSCVMotherboard.IOE1_PORT1, FSCVMotherboard.COND_EN_D),
		}
		port, mask = switcher.get(channelEn, (None, None))
		if port is not None and mask is not None:
			self.values[port] |= mask

	def enableIREFTEST(self, channelEn):
		switcher = {
			FSCVMotherboard.CH_12: (FSCVMotherboard.MCU_PORT3, FSCVMotherboard.IREF_TEST_12),
			FSCVMotherboard.CH_1: (FSCVMotherboard.MCU_PORT3, FSCVMotherboard.IREF_TEST_12),
			FSCVMotherboard.CH_2: (FSCVMotherboard.MCU_PORT3, FSCVMotherboard.IREF_TEST_12),
			FSCVMotherboard.CH_34: (FSCVMotherboard.IOE2_PORT1, FSCVMotherboard.IREF_TEST_34),
			FSCVMotherboard.CH_3: (FSCVMotherboard.IOE2_PORT1, FSCVMotherboard.IREF_TEST_34),
			FSCVMotherboard.CH_4: (FSCVMotherboard.IOE2_PORT1, FSCVMotherboard.IREF_TEST_34),
			FSCVMotherboard.CH_56: (FSCVMotherboard.IOE1_PORT1, FSCVMotherboard.IREF_TEST_56),
			FSCVMotherboard.CH_5: (FSCVMotherboard.IOE1_PORT1, FSCVMotherboard.IREF_TEST_56),
			FSCVMotherboard.CH_6: (FSCVMotherboard.IOE1_PORT1, FSCVMotherboard.IREF_TEST_56),
			FSCVMotherboard.CH_78: (FSCVMotherboard.MCU_PORT6, FSCVMotherboard.IREF_TEST_78),
			FSCVMotherboard.CH_7: (FSCVMotherboard.MCU_PORT6, FSCVMotherboard.IREF_TEST_78),
			FSCVMotherboard.CH_8: (FSCVMotherboard.MCU_PORT6, FSCVMotherboard.IREF_TEST_78),
			FSCVMotherboard.CH_DE: (FSCVMotherboard.IOE1_PORT1, FSCVMotherboard.IREF_TEST_D),
		}
		port, mask = switcher.get(channelEn, (None, None))
		if port is not None and mask is not None:
			self.values[port] |= mask

	def enableChannel(self, channelEn):
		switcher = {
			FSCVMotherboard.CH_1: (FSCVMotherboard.MCU_PORT6, FSCVMotherboard.CH_EN_1),
			FSCVMotherboard.CH_2: (FSCVMotherboard.MCU_PORT3, FSCVMotherboard.CH_EN_2),
			FSCVMotherboard.CH_3: (FSCVMotherboard.IOE2_PORT1, FSCVMotherboard.CH_EN_3),
			FSCVMotherboard.CH_4: (FSCVMotherboard.IOE2_PORT0, FSCVMotherboard.CH_EN_4),
			FSCVMotherboard.CH_5: (FSCVMotherboard.IOE2_PORT0, FSCVMotherboard.CH_EN_5),
			FSCVMotherboard.CH_6: (FSCVMotherboard.MCU_PORT6, FSCVMotherboard.CH_EN_6),
			FSCVMotherboard.CH_7: (FSCVMotherboard.IOE1_PORT0, FSCVMotherboard.CH_EN_7),
			FSCVMotherboard.CH_8: (FSCVMotherboard.IOE1_PORT0, FSCVMotherboard.CH_EN_8),
			FSCVMotherboard.CH_DE: (FSCVMotherboard.IOE1_PORT0, FSCVMotherboard.CH_EN_D),
		}
		port, mask = switcher.get(channelEn, (None, None))
		if port is not None and mask is not None:
			self.values[port] |= mask

	def enableVDD(self, channelEn):
		switcher = {
			FSCVMotherboard.CH_12: (FSCVMotherboard.IOE1_PORT0, FSCVMotherboard.EN_12),
			FSCVMotherboard.CH_1: (FSCVMotherboard.IOE1_PORT0, FSCVMotherboard.EN_12),
			FSCVMotherboard.CH_2: (FSCVMotherboard.IOE1_PORT0, FSCVMotherboard.EN_12),
			FSCVMotherboard.CH_34: (FSCVMotherboard.IOE2_PORT1, FSCVMotherboard.EN_34),
			FSCVMotherboard.CH_3: (FSCVMotherboard.IOE2_PORT1, FSCVMotherboard.EN_34),
			FSCVMotherboard.CH_4: (FSCVMotherboard.IOE2_PORT1, FSCVMotherboard.EN_34),
			FSCVMotherboard.CH_56: (FSCVMotherboard.IOE2_PORT0, FSCVMotherboard.EN_56),
			FSCVMotherboard.CH_5: (FSCVMotherboard.IOE2_PORT0, FSCVMotherboard.EN_56),
			FSCVMotherboard.CH_6: (FSCVMotherboard.IOE2_PORT0, FSCVMotherboard.EN_56),
			FSCVMotherboard.CH_78: (FSCVMotherboard.MCU_PORT3, FSCVMotherboard.EN_78),
			FSCVMotherboard.CH_7: (FSCVMotherboard.MCU_PORT3, FSCVMotherboard.EN_78),
			FSCVMotherboard.CH_8: (FSCVMotherboard.MCU_PORT3, FSCVMotherboard.EN_78),
			FSCVMotherboard.CH_DE: (FSCVMotherboard.IOE1_PORT1, FSCVMotherboard.EN_D),
		}
		port, mask = switcher.get(channelEn, (None, None))
		if port is not None and mask is not None:
			self.values[port] |= mask

	def enableIREF(self, channelEn):
		switcher = {
			FSCVMotherboard.CH_12: (FSCVMotherboard.MCU_PORT7, FSCVMotherboard.IREF_EN_12),
			FSCVMotherboard.CH_1: (FSCVMotherboard.MCU_PORT7, FSCVMotherboard.IREF_EN_12),
			FSCVMotherboard.CH_2: (FSCVMotherboard.MCU_PORT7, FSCVMotherboard.IREF_EN_12),
			FSCVMotherboard.CH_34: (FSCVMotherboard.IOE2_PORT1, FSCVMotherboard.IREF_EN_34),
			FSCVMotherboard.CH_3: (FSCVMotherboard.IOE2_PORT1, FSCVMotherboard.IREF_EN_34),
			FSCVMotherboard.CH_4: (FSCVMotherboard.IOE2_PORT1, FSCVMotherboard.IREF_EN_34),
			FSCVMotherboard.CH_56: (FSCVMotherboard.IOE1_PORT1, FSCVMotherboard.IREF_EN_56),
			FSCVMotherboard.CH_5: (FSCVMotherboard.IOE1_PORT1, FSCVMotherboard.IREF_EN_56),
			FSCVMotherboard.CH_6: (FSCVMotherboard.IOE1_PORT1, FSCVMotherboard.IREF_EN_56),
			FSCVMotherboard.CH_78: (FSCVMotherboard.MCU_PORT7, FSCVMotherboard.IREF_EN_78),
			FSCVMotherboard.CH_7: (FSCVMotherboard.MCU_PORT7, FSCVMotherboard.IREF_EN_78),
			FSCVMotherboard.CH_8: (FSCVMotherboard.MCU_PORT7, FSCVMotherboard.IREF_EN_78),
			FSCVMotherboard.CH_DE: (FSCVMotherboard.IOE1_PORT1, FSCVMotherboard.IREF_EN_D),
		}
		port, mask = switcher.get(channelEn, (None, None))
		if port is not None and mask is not None:
			self.values[port] |= mask


	def initIref(self, channelName, data):
		if data[CurrentGeneration.IREF_TEST_EN]:
			self.enableIREFTEST(channelName)
		if data[CurrentGeneration.IREF_EN]:
			self.enableIREF(channelName)

	def initPR(self, data):
		if data[PR.SEL_1]:
			self.values[FSCVMotherboard.IOE2_PORT0]|=FSCVMotherboard.SEL1_PR
		if data[PR.SEL_2]:
			self.values[FSCVMotherboard.IOE2_PORT0]|=FSCVMotherboard.SEL2_PR
		if data[PR.SEL_3]:
			self.values[FSCVMotherboard.IOE2_PORT0]|=FSCVMotherboard.SEL3_PR
		if data[PR.IREF_SWITCH_SEL]:
			self.values[FSCVMotherboard.IOE2_PORT0]|=FSCVMotherboard.IREF_SWITCH_PR
