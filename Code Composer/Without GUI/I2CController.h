#ifndef I2C_CONTROLLER_H
#define I2C_CONTROLLER_H

// Function prototypes
void init_CLK(void);
void init_I2C(void);
void write_I2C_byte(unsigned int slave_addr, unsigned int reg_addr, unsigned int data);


#endif /* I2C_CONTROLLER_H */
