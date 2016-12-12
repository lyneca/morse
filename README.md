# Morse
Scripts for morse translation from serial COM ports.

Both scripts use COM3 (Windows) by default and have Tk GUIs.

## Dependencies
 - [`keyboard`](https://pypi.python.org/pypi/keyboard/)
 - [`pyserial`](https://pypi.python.org/pypi/pyserial/)
 
## To Keypress
`serial_to_keyboard.pyw` converts the serial signal into a keypress uses the [keyboard] library.
## To Letters
`translate.pyw` translates serial signal into letters.
Uses standard [Morse international duration ratios](https://en.wikipedia.org/wiki/Morse_code#Representation.2C_timing_and_speeds):
 - dah = 3x dit
 - character space = 3x dit
 - word space = 7x dit.

Hence to change the speed change the dit length:

```python
dit_length = 0.1  # seconds
```

Default = `100ms`.
