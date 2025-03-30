import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Initialisation du clavier HID
keyboard = Keyboard(usb_hid.devices)

# Définition de la matrice des touches
matrix_keys = [
    [Keycode.ESCAPE, Keycode.F1, Keycode.F2, Keycode.F3, Keycode.F4],
    [Keycode.GRAVE_ACCENT, Keycode.ONE, Keycode.EIGHT, Keycode.NINE, Keycode.ZERO],
    [Keycode.A, Keycode.B, Keycode.C, Keycode.D, Keycode.E],
    [Keycode.F, Keycode.G, Keycode.H, Keycode.I, Keycode.J],
    [Keycode.K, Keycode.L, Keycode.M, Keycode.N, Keycode.O, Keycode.P, Keycode.Q],
    [Keycode.LEFT_CONTROL, Keycode.GUI, Keycode.M, Keycode.N, Keycode.O]
]

# pins used for columns (outputs)
keypad_rows = [
    board.GP18,
    board.GP19,
    board.GP20,
    board.GP21,
    board.GP22,
    board.GP23
]

# pins used for rows (inputs)
keypad_cols = [
    board.GP17,
    board.GP16,
    board.GP15,
    board.GP14,
    board.GP13,
    board.GP12
]

# Configuration des broches des colonnes
cols = []
for col_pin in keypad_cols:
    col = digitalio.DigitalInOut(col_pin)
    col.direction = digitalio.Direction.OUTPUT
    col.value = False  # Par défaut, les colonnes sont désactivées
    cols.append(col)

# Configuration des broches des rangées
rows = []
for row_pin in keypad_rows:
    row = digitalio.DigitalInOut(row_pin)
    row.direction = digitalio.Direction.INPUT
    row.pull = digitalio.Pull.DOWN  # Active le pull-down interne
    rows.append(row)

# Suivi de l'état des touches
previous_state = [[False] * len(cols) for _ in range(len(rows))]

# Fonction pour scanner la matrice
def scan_matrix():
    current_state = [[False] * len(cols) for _ in range(len(rows))]
    for col_index, col in enumerate(cols):
        col.value = True  # Activer une colonne
        for row_index, row in enumerate(rows):
            if row.value:  # Si un bouton est pressé
                current_state[row_index][col_index] = True
        col.value = False  # Désactiver la colonne
    return current_state

# Boucle principale
while True:
    current_state = scan_matrix()
    for row_index, row in enumerate(current_state):
        for col_index, pressed in enumerate(row):
            # Si une touche est pressée et n'était pas pressée auparavant
            if pressed and not previous_state[row_index][col_index]:
                key = matrix_keys[row_index][col_index]
                print(f"ON {key} ({row_index}, {col_index})")
                keyboard.press(key)  # Simule une pression de touche

            # Si une touche était pressée et ne l'est plus
            elif not pressed and previous_state[row_index][col_index]:
                key = matrix_keys[row_index][col_index]
                print(f"OF {key} ({row_index}, {col_index})")
                keyboard.release(key)  # Relâche explicitement la touche

    # Mettre à jour l'état précédent
    previous_state = current_state
