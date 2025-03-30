import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import time

class Config:
    CHECK_CIRCUIT_CUT = False
    REAL_PRESS = True

# Initialisation du clavier HID
keyboard = Keyboard(usb_hid.devices)

# Définition de la matrice des touches
matrix_keys = [
    [Keycode.ESCAPE, Keycode.F1, Keycode.F2, Keycode.F3, Keycode.F4, Keycode.F5, Keycode.F6, Keycode.F7, Keycode.F8, Keycode.F9, Keycode.F10, Keycode.F11, Keycode.F12, Keycode.PRINT_SCREEN, Keycode.PAUSE, Keycode.DELETE],
    [Keycode.GRAVE_ACCENT, Keycode.ONE, Keycode.TWO, Keycode.THREE, Keycode.FOUR, Keycode.FIVE, Keycode.SIX, Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE, Keycode.ZERO, Keycode.MINUS, None, Keycode.EQUALS, Keycode.BACKSPACE, Keycode.HOME],
    [Keycode.A, Keycode.B, Keycode.C, Keycode.D, Keycode.E],
    [Keycode.F, Keycode.G, Keycode.H, Keycode.I, Keycode.J],
    [Keycode.K, Keycode.L, Keycode.M, Keycode.N, Keycode.O, Keycode.P, Keycode.Q],
    [Keycode.LEFT_CONTROL, Keycode.GUI, Keycode.M, Keycode.N, Keycode.O]
]

# Inverser la liste des touches dans la matrice
matrix_keys = matrix_keys[::-1]

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
    board.GP12,
    board.GP11,
    board.GP10,
    board.GP9,
    board.GP8,
    board.GP7,
    board.GP6,
    board.GP5,
    board.GP4,
    board.GP3,
    board.GP2,
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

print("📌 Liste des broches des rangées :", keypad_rows)
print("📌 Liste des broches des colonnes :", keypad_cols)

def check_for_short_circuit():
    print("🔍 Vérification des pins en cours...")
    time.sleep(5)

    short_circuits = []

    initial_state = scan_matrix()
    for row_index, row in enumerate(initial_state):
        for col_index, pressed in enumerate(row):
            if pressed:
                short_circuits.append((keypad_rows[row_index], keypad_cols[col_index]))

    if short_circuits:
        print("⚠️ Erreur : Court-circuit détecté ! Vérifiez votre câblage.")
        for row_pin, col_pin in short_circuits:
            print(f"🔴 Court-circuit entre {row_pin} et {col_pin}")
    else:
        print("✅ Aucun court-circuit détecté.")

if Config.CHECK_CIRCUIT_CUT:
    check_for_short_circuit()

# Boucle principale
while True:
    current_state = scan_matrix()
    for row_index, row in enumerate(current_state):
        for col_index, pressed in enumerate(row):
            if pressed and not previous_state[row_index][col_index]:
                # Vérifie si la touche existe dans la matrice
                if row_index < len(matrix_keys) and col_index < len(matrix_keys[row_index]):
                    key = matrix_keys[row_index][col_index]
                    print(f"ON {key} ({row_index}, {col_index})")
                    if Config.REAL_PRESS:
                        keyboard.press(key)
                else:
                    print(f"⚠️ {row_index}, {col_index} n'a pas de touche associée.")

            elif not pressed and previous_state[row_index][col_index]:
                # Vérifie si la touche existe dans la matrice
                if row_index < len(matrix_keys) and col_index < len(matrix_keys[row_index]):
                    key = matrix_keys[row_index][col_index]
                    print(f"OF {key} ({row_index}, {col_index})")
                    if Config.REAL_PRESS:
                        keyboard.release(key)
    
    # Mettre à jour l'état précédent
    previous_state = current_state
