import pcd8544
from machine import Pin, SPI
from hx711 import HX711
from utime import sleep_us

spi = SPI(2)
spi.init(baudrate=2000000, polarity=1, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
cs = Pin(5)
dc = Pin(15)
rst = Pin(4)
bl = Pin(12, Pin.OUT, value=1)

lcd = pcd8544.PCD8544(spi, cs, dc, rst)

import framebuf
buffer = bytearray((pcd8544.HEIGHT // 8) * pcd8544.WIDTH)

lcd.data(buffer)


class Scales(HX711):
    def __init__(self, d_out, pd_sck):
        super(Scales, self).__init__(d_out, pd_sck)
        self.offset = 0

    def reset(self):
        self.power_off()
        self.power_on()

    def tare(self):
        self.offset = self.read()

    def raw_value(self):
        return self.read() - self.offset

    def stable_value(self, reads=10, delay_us=500):
        values = []
        for _ in range(reads):
            values.append(self.raw_value())
            sleep_us(delay_us)
        return self._stabilizer(values)

    @staticmethod
    def _stabilizer(values, deviation=10):
        weights = []
        for prev in values:
            weights.append(sum([1 for current in values if abs(prev - current) / (prev / 100) <= deviation]))
        return sorted(zip(values, weights), key=lambda x: x[1]).pop()[0]

while True:
    scales = Scales(d_out=16, pd_sck=17)
    scales.tare()
    val = scales.raw_value()
    print(val)
    print(scales.offset)