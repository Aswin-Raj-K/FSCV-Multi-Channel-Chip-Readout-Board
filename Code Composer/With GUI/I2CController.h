#ifndef I2C_CONTROLLER_H
#define I2C_CONTROLLER_H

// Function prototypes

void initI2C(void);
void writeI2CByte(unsigned int slave_addr, unsigned int reg_addr, unsigned int data);


#endif /* I2C_CONTROLLER_H */
