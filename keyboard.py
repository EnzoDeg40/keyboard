from machine import Pin
import utime

matrix_keys = [
    ['1', '2'],
    ['3', '4']
]

keypad_cols = [25, 24]
keypad_rows = [0, 1]

col_pins = []
row_pins = []

for x in range(0, 2):
    row_pins.append(Pin(keypad_rows[x], Pin.OUT))
    row_pins[x].value(1)
    col_pins.append(Pin(keypad_cols[x], Pin.IN, Pin.PULL_DOWN))
    col_pins[x].value(0)
    
print("Please press a key")

def scankeys():
    for row in range(2):
        for col in range(2):
            row_pins[row].high()
            key = None

            if col_pins[col].value() == 1:
                print("You have pressed:", matrix_keys[row][col])
                key_press = matrix_keys[row][col]
                utime.sleep(0.3)

            row_pins[row].low()

while True:
    scankeys()
