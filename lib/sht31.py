import smbus
import time

class SHT31:
    def __init__(self, address, channel):
        self.address    = address
        self.channel    = channel
        self.bus        = smbus.SMBus(self.channel)
        self.bus.write_i2c_block_data(self.address, 0x2C, [0x06])
        time.sleep(0.5)

    def read(self):
        raw = self.bus.read_i2c_block_data(self.address, 0x00, 6)
        temp = raw[0] * 256 + raw[1]
        cTemp = -45 + (175 * temp / 65535.0)
        #fTemp = -49 + (315 * temp / 65535.0)
        humidity = 100 * (raw[3] * 256 + raw[4]) / 65535.0

        return (cTemp, humidity)

if __name__ == '__main__':
    sensor = SHT31(0x45, 1)
    data = sensor.read()
    print('Temperature: %s' % round(data[0],2))
    print('Humidity:    %s' % round(data[1],2))
