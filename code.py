import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Initialisation du clavier HID
keyboard = Keyboard(usb_hid.devices)

# Définition de la matrice des touches
matrix_keys = [
    [Keycode.ONE, Keycode.TWO, Keycode.THREE, Keycode.FOUR, Keycode.FIVE],
    [Keycode.SIX, Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE, Keycode.ZERO],
    [Keycode.A, Keycode.B, Keycode.C, Keycode.D, Keycode.E],
    [Keycode.F, Keycode.G, Keycode.H, Keycode.I, Keycode.J],
    [Keycode.K, Keycode.L, Keycode.M, Keycode.N, Keycode.O]
]

# Broches utilisées pour les colonnes (sorties)
keypad_rows = [board.GP25, board.GP24, board.GP23, board.GP22, board.GP21]
# Broches utilisées pour les rangées (entrées)
keypad_cols = [board.GP0, board.GP1, board.GP3, board.GP4, board.GP5]

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

# Fonction pour scanner la matrice
def scan_matrix():
    for col_index, col in enumerate(cols):
        col.value = True  # Activer une colonne
        # print(f"Colonne {col_index} activée")
        for row_index, row in enumerate(rows):
            if row.value:  # Si un bouton est pressé
                print(f"  → Touche détectée : Colonne {col_index}, Rangée {row_index}")
                col.value = False  # Désactiver la colonne avant de sortir
                return col_index, row_index
        col.value = False  # Désactiver la colonne
    return None, None

# Boucle principale
while True:
    col, row = scan_matrix()
    if col is not None and row is not None:
        key = matrix_keys[row][col]
        print(f"Envoi de la touche : {key}")  # Affiche la touche envoyée
        keyboard.press(key)  # Simule une pression de touche
        keyboard.release_all()  # Relâche toutes les touches
