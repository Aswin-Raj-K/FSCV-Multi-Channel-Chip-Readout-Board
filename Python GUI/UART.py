import serial
import time


class UART():
	BAUD_RATE = 9600
	PORT = "COM4"
	UART_SUCCESS = "SUCCESS"
	UART_FAILED = "FAILED"
	def __init__(self):
		self.baudRate = UART.BAUD_RATE
		self.port = UART.PORT

	def getPort(self):
		return self.port

	def getBaudRate(self):
		return self.baudRate

	def uartSendReceive(self, packet, timeout=1):
		try:
			# Open the serial port
			ser = serial.Serial(self.port, self.baudRate, timeout=timeout)

			# Print port information
			print("Port opened successfully: " + ser.name)

			ser.write(packet)

			# Wait for a brief moment
			time.sleep(0.1)

			# Read data
			received_data = ser.readline().decode('utf-8')

			# Print received data
			print("Received data: " + received_data.strip())

			# Close the serial port
			ser.close()
			print("Port closed successfully")

			return received_data.strip()

		except serial.SerialException as e:
			print("Error: " + str(e))
			return UART.UART_FAILED
