"""
``pn532.i2c``
====================================================

This module will let you communicate with a PN532 RFID/NFC shield or breakout
using I2C.

* Author(s): Original Raspberry Pi code by Tony DiCola, CircuitPython by ladyada,
             refactor by Carter Nelson, MicroPython by Olaf van der Kruk

"""
import time
from pn532 import PN532, BusyError


class PN532_I2C(PN532):
    """Driver for the PN532 connected over I2C"""

    def __init__(self, i2c, *, reset=None, debug=False, address=0x24):
      """Create an instance of the PN532 class using Serial connection.
      Optional reset pin and debugging output.
      """
      self.debug = debug
      self._i2c = i2c
      self._i2c_addr = address
      super().__init__(debug=debug, reset=reset)

    def _wakeup(self):
      """Send any special commands/data to wake up PN532"""
      if self.debug:
        print("Waking up")
      if self._reset_pin:
          self._reset_pin.value = True
          time.sleep(0.01)
      self.low_power = False
      #self._i2c.writeto(self._i2c_addr,
      #    b"\x55\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
      #)  # wake up!
      self.SAM_configuration()

    def _wait_ready(self, timeout=1000):
      """Wait `timeout` milliseconds"""
      status = bytearray(1)
      start = time.ticks_ms()
      while time.ticks_diff(time.ticks_ms(), start) < timeout:
        try:
          self._i2c.readfrom_into(self._i2c_addr, status)
        except OSError:
          continue
        if status == b"\x01":
          return True  # No longer busy
        time.sleep(0.01)  # lets ask again soon!
      # Timed out!
      return False

    def _read_data(self, count):
      """Read a specified count of bytes from the PN532."""
      frame = bytearray(count + 1)
      self._i2c.readfrom_into(self._i2c_addr, frame)
      if not frame:
          raise BusyError("No data read from PN532")
      if self.debug:
          print("Reading: ", [hex(i) for i in frame])
      return frame[1:]

    def _write_data(self, framebytes):
      """Write a specified count of bytes to the PN532"""
      self._i2c.writeto(self._i2c_addr, framebytes)