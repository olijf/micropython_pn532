# PN532 driver for MicroPython
MicroPython driver for PN532 NFC/RFID breakout boards. Based on the [CircuitPython driver by Adafruit](https://github.com/adafruit/Adafruit_CircuitPython_PN532).

### Compatibility
This driver has only been tested with the ESP32 and RP2040 using the [Grove NFC breakout board](https://wiki.seeedstudio.com/Grove_NFC/) and the cheap Aliexpress modules in the default UART mode and I2C mode. 

Please let me know if you get this module successfully working with other hardware.

### Usage
You can install the package using `mpremote` with the following command:
```bash
mpremote mip install "github:olijf/micropython_pn532/pn532"
```


```python
from machine import Pin, I2C

i2c = I2C(0, scl=Pin(5), sda=Pin(4))

from i2c import PN532_I2C
pn532 = PN532_I2C(i2c, debug=True)

uid = pn532.read_passive_target(timeout=500)

if uid is None:
  print("No card detected")
else:
  print("Found card with UID:", [hex(i) for i in uid])
```

### Differences in the API from the CircuitPython version

- The timeout is expressed in milliseconds instead of seconds.
- The module name is different.
- Only UART and I2C is available
- _SPI is not available._ 

### TODO
- [ ] Implement SPI
- [ ] Rewrite the modules with asyncio support so we can use the library non blocking
- [ ] Determine if thread blocking is really an issue when used
- [ ] Add support for the other modes of the PN532, card emulation specifically

