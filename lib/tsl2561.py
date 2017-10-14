import smbus
import time


class TSL2561:
    def __init__(self, address, channel):
        self.address = address
        self.channel = channel
        self.bus = smbus.SMBus(self.channel)
        self.bus.write_i2c_block_data(self.address, 0x80, [0x03])
        time.sleep(0.5)

    def read(self):
        vlrd_data = self.bus.read_i2c_block_data(self.address, 0xAC, 2)
        VLRD = vlrd_data[1] << 8 | vlrd_data[0]
        irrd_data = self.bus.read_i2c_block_data(self.address, 0xAE, 2)
        IRRD = irrd_data[1] << 8 | irrd_data[0]

        if (float(VLRD) == 0):
            ratio = 9999
        else:
            ratio = (IRRD / float(VLRD))

        if ((ratio >= 0) & (ratio <= 0.52)):
            lux = (0.0315 * VLRD) - (0.0593 * VLRD * (ratio**1.4))
        elif (ratio <= 0.65):
            lux = (0.0229 * VLRD) - (0.0291 * IRRD)
        elif (ratio <= 0.80):
            lux = (0.0157 * VLRD) - (0.018 * IRRD)
        elif (ratio <= 1.3):
            lux = (0.00338 * VLRD) - (0.0026 * IRRD)
        elif (ratio > 1.3):
            lux = 0

        return (lux, None)

if __name__ == '__main__':
    sensor = TSL2561(0x39, 1)
    data = sensor.read()
    print('Luminosity:  %s' % round(data[0], 2))
