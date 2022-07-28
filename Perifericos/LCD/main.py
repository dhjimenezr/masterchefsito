import pcd8544
import dht
from machine import Pin, SPI, I2C
import framebuf
from time import sleep

sensor = dht.DHT11(Pin(16))

spi = SPI(2)
spi.init(baudrate=8000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23))
cs = Pin(5)
dc = Pin(15)
rst = Pin(4)
bl = Pin(12, Pin.OUT, value=1)

lcd = pcd8544.PCD8544(spi, cs, dc, rst)

buffer = bytearray((lcd.height // 8) * lcd.width)
framebuf = framebuf.FrameBuffer1(buffer, lcd.width, lcd.height)
framebuf.fill(1)
framebuf.fill(0)

# while True:
#     try:
#         sleep(2)
#         bl.value(0)
#         lcd.clear()
#         sensor.measure()
#         temp = sensor.temperature()
#         hum = sensor.humidity()
#         framebuf.text("TEMPERATURA", 0, 0, 1)
#         framebuf.text(temp, 0, 9, 1)
#         framebuf.text("HUMEDAD", 0, 17, 1)
#         framebuf.text(hum, 0, 25, 1)
#         framebuf.text("12345678", 0, 33, 1)
#         framebuf.text("ABCDEF", 0, 41, 1)
#         lcd.data(buffer)
#     except OSError as e:
bl.value(0)
lcd.clear()
framebuf.text("TEMP", 0, 0, 1)
framebuf.text("No sensor", 0, 9, 1)
framebuf.text("HUMEDAD", 0, 17, 1)
framebuf.text("No sensor", 0, 25, 1)
framebuf.text("1234567890", 0, 33, 1)
framebuf.text("ABCDEFGHIJ", 0, 41, 1)
lcd.data(buffer)