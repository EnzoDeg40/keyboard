from machine import Pin
import utime

matrix_keys = [
    ['1', '2', '3', '4', '5'],
    ['6', '7', '8', '9', '10'],
    ['11', '12', '13', '14', '15'],
    ['16', '17', '18', '19', '20'],
    ['21', '22', '23', '24', '25']
]

keypad_cols = [25, 24, 23, 22, 21]
keypad_rows = [0, 1, 3, 4, 5]

col_pins = []
row_pins = []

for x in range(0, 5):
    row_pins.append(Pin(keypad_rows[x], Pin.OUT))
    row_pins[x].value(1)
    col_pins.append(Pin(keypad_cols[x], Pin.IN, Pin.PULL_DOWN))
    col_pins[x].value(0)
    
print("Please press a key")

def scankeys():
    for row in range(5):
        for col in range(5):
            row_pins[row].high()
            key = None

            if col_pins[col].value() == 1:
                print("You have pressed:", matrix_keys[row][col])
                key_press = matrix_keys[row][col]
                utime.sleep(0.3)

            row_pins[row].low()

while True:
    scankeys()
