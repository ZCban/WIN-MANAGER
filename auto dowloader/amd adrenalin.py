import webbrowser
import pyautogui
import time
import os

download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
file_path = os.path.join(download_folder, "amd-adrenalin.exe")

# Controlla se il file esiste
if os.path.exists(file_path):
    print(f"File '{file_path}' già presente. Eliminazione in corso...")
    os.remove(file_path)
    print("File eliminato.")
else:
    print("File non presente. Procedo con il download.")

# URL da aprire
url = "https://www.amd.com/en/support/downloads/drivers.html/graphics/radeon-rx/radeon-rx-7000-series/amd-radeon-rx-7900-xtx.html"


# Apri il browser predefinito all'indirizzo specificato
webbrowser.open(url)


# Specifica il percorso all'immagine
image_path = "button_img/amd-adrenalin/11.jpg"#win11
adrenalin_box_path = "button_img/amd-adrenalin/adrenalin-edition.jpg"  # Immagine del riquadro "Adrenalin Edition"
download_button_path = "button_img/amd-adrenalin/download.jpg"  # Immagine del pulsante "Download"
directory_download_path = "button_img/amd-adrenalin/directory-download.jpg"  # Immagine della directory "Download"
filename_field_path = "button_img/amd-adrenalin/nome-file.jpg"  # Immagine del campo del nome del file
save_button_path = "button_img/amd-adrenalin/salva.jpg"  # Immagine del pulsante "Salva"

# Attendi un breve periodo per dare tempo al browser di caricarsi
time.sleep(2)

# Trova la posizione dell'immagine sullo schermo
button_location = pyautogui.locateOnScreen(image_path, confidence=0.8)

if button_location:
    # Calcola il centro del pulsante
    button_center = pyautogui.center(button_location)
    
    # Sposta il cursore e clicca
    pyautogui.moveTo(button_center)
    pyautogui.click()
    print("Cliccato sul pulsante.")
else:
    print("Immagine non trovata sullo schermo.")

time.sleep(1)
# Trova la posizione del riquadro "Adrenalin Edition"
adrenalin_box_location = pyautogui.locateOnScreen(adrenalin_box_path, confidence=0.8)

if adrenalin_box_location:
    print("Riquadro 'Adrenalin Edition' trovato.")
    
    # Limita l'area di ricerca al riquadro individuato
    region = (
        adrenalin_box_location.left,
        adrenalin_box_location.top,
        adrenalin_box_location.width,
        adrenalin_box_location.height
    )

    time.sleep(0.5)
    # Trova il pulsante "Download" all'interno del riquadro
    download_button_location = pyautogui.locateOnScreen(download_button_path, region=region, confidence=0.8)
    
    if download_button_location:
        print("Pulsante 'Download' trovato.")
        
        # Calcola il centro del pulsante "Download"
        button_center = pyautogui.center(download_button_location)
        
        # Sposta il cursore e clicca
        pyautogui.moveTo(button_center)
        pyautogui.click()
        print("Cliccato sul pulsante 'Download'.")


    else:
        print("Pulsante 'Download' non trovato all'interno del riquadro.")
else:
    print("Riquadro 'Adrenalin Edition' non trovato.")

time.sleep(0.5)
# Trova l'immagine della directory "Download" e cliccaci sopra
download_location = pyautogui.locateOnScreen(directory_download_path, confidence=0.8)
if download_location:
    pyautogui.moveTo(pyautogui.center(download_location))
    pyautogui.click()
    print("Cliccato sulla directory 'Download'.")
else:
    print("Directory 'Download' non trovata.")

time.sleep(0.5)
# Trova il campo del nome del file e scrivi "amd-adrenalin"
filename_location = pyautogui.locateOnScreen(filename_field_path, confidence=0.8)
if filename_location:
    pyautogui.moveTo(pyautogui.center(filename_location))
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')  # Seleziona tutto il testo
    pyautogui.press('backspace')  # Cancella il testo selezionato
    pyautogui.write("amd-adrenalin")
    print("Nome file inserito: 'amd-adrenalin'.")
else:
    print("Campo del nome del file non trovato.")

time.sleep(0.5)
# Trova il pulsante "Salva" e cliccaci sopra
save_button_location = pyautogui.locateOnScreen(save_button_path, confidence=0.8)
if save_button_location:
    pyautogui.moveTo(pyautogui.center(save_button_location))
    pyautogui.click()
    print("Cliccato sul pulsante 'Salva'.")
else:
    print("Pulsante 'Salva' non trovato.")
