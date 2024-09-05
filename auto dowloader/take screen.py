import numpy as np
import cv2
import os
from mss import mss
import ctypes
from ctypes import wintypes

# Inizializza la cattura dello schermo
screen_capture = mss()

# API di Windows per il rilevamento del tasto del mouse
user32 = ctypes.WinDLL('user32', use_last_error=True)
VK_MBUTTON = 0x05  # Codice del tasto centrale del mouse

# Funzione per catturare e salvare lo screenshot
def take_screenshot():
    # Cattura lo schermo intero
    screen_region = screen_capture.monitors[1]  # Cattura l'intero primo monitor
    img = np.array(screen_capture.grab(screen_region))
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # Ottieni il percorso della directory corrente
    current_directory = os.path.dirname(os.path.abspath(__file__))
    output_file_path = os.path.join(current_directory, 'screenshot.jpg')

    # Salva l'immagine nella directory corrente
    cv2.imwrite(output_file_path, img)
    print(f"Immagine salvata in: {output_file_path}")

# Ciclo principale che controlla la pressione del tasto
print("Premi la rotellina del mouse per scattare uno screenshot.")
try:
    while True:
        # Controlla se il tasto centrale del mouse è premuto
        if user32.GetAsyncKeyState(VK_MBUTTON) & 0x8000:
            take_screenshot()
            while user32.GetAsyncKeyState(VK_MBUTTON) & 0x8000:
                pass  # Attende che il tasto venga rilasciato per evitare scatti multipli
except KeyboardInterrupt:
    print("Programma terminato.")
