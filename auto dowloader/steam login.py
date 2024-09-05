import subprocess
import os
import psutil
import pygetwindow as gw
import time
import pyautogui
import pyperclip

# Specifica il percorso completo dell'eseguibile di Steam
steam_path = "C:\\Program Files (x86)\\Steam\\Steam.exe"

# Specifica il percorso alle immagini
utente_path = "button_img/steam/utente-steam.jpg"
pass_path = "button_img/steam/pass-steam.jpg"
ricorda_path = "button_img/steam/ricordami-steam.jpg"
accedi_download_path = "button_img/steam/accedi-steam.jpg"

# Credenziali
username = ""
password = ""

# Funzione per controllare se il processo di Steam è in esecuzione
def is_steam_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == "Steam.exe":
            return True
    return False

# Funzione per controllare se la finestra di Steam è aperta
def is_steam_window_open():
    windows = gw.getAllTitles()
    for window in windows:
        if "Steam" in window:
            return True
    return False

def type_password(password):
    for char in password:
        if char.isupper():
            pyautogui.keyDown('shift')
            pyautogui.press(char.lower())
            pyautogui.keyUp('shift')
        elif char in "!@#$%^&*()_+{}|:\"<>?":
            pyautogui.keyDown('shift')
            pyautogui.press(char)
            pyautogui.keyUp('shift')
        else:
            pyautogui.press(char)


# Avvia Steam se non è già in esecuzione
if not is_steam_running():
    if os.path.exists(steam_path):
        subprocess.Popen([steam_path])
        print("Steam è stato avviato.")
    else:
        print("Il percorso specificato non esiste. Verifica il percorso di Steam.")
        exit()

# Continua a cercare la finestra di Steam fino a quando non è aperta
print("In attesa che la finestra di Steam si apra...")

while not is_steam_window_open():
    time.sleep(2)  # Attende 1 secondo prima di controllare di nuovo

print("La finestra di Steam è aperta.")

time.sleep(1)
# Cerca e clicca sull'elemento "Utente"
utente_location = pyautogui.locateCenterOnScreen(utente_path,confidence=0.8)
if utente_location:
    pyautogui.click(utente_location)
    print("Cliccato sul campo 'Utente'.")
    pyautogui.write(username)  # Scrive il nome utente
    print(f"Nome utente '{username}' inserito.")

# Cerca e clicca sull'elemento "Password"
pass_location = pyautogui.locateCenterOnScreen(pass_path,confidence=0.8)
if pass_location:
    pyautogui.click(pass_location)
    print("Cliccato sul campo 'Password'.")
    # Copia la password negli appunti
    pyperclip.copy(password)
    # Dopo aver cliccato sul campo "Password"
    pyautogui.hotkey('ctrl', 'v')  # Incolla la password
    print("Password inserita.")


# Cerca e clicca sul pulsante "Accedi"
accedi_location = pyautogui.locateCenterOnScreen(accedi_download_path,confidence=0.8)
if accedi_location:
    pyautogui.click(accedi_location)
    print("Cliccato su 'Accedi'.")

