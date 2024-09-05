import os
import zipfile
import tempfile
import shutil
import subprocess
import win32api
import pywintypes
import win32con
import time
import sys

# Nome del file ZIP incluso nell'eseguibile
ZIP_FILE_NAME = "QRes.zip"

# Funzione per estrarre il file ZIP nella directory temporanea
def extract_zip_to_temp():
    # Crea una directory temporanea
    temp_dir = tempfile.mkdtemp()

    # Ottieni il percorso del file ZIP all'interno dell'eseguibile
    zip_path = os.path.join(sys._MEIPASS, ZIP_FILENAME) if getattr(sys, 'frozen', False) else ZIP_FILE_NAME

    # Estrai il file ZIP nella directory temporanea
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    return temp_dir

# Funzione per ottenere la risoluzione e il refresh rate attuali
def get_current_resolution_and_refresh_rate():
    device_name = win32api.EnumDisplayDevices(None, 0).DeviceName
    try:
        mode = win32api.EnumDisplaySettings(device_name, win32con.ENUM_CURRENT_SETTINGS)
        resolution = (mode.PelsWidth, mode.PelsHeight)
        refresh_rate = mode.DisplayFrequency
        return resolution, refresh_rate
    except pywintypes.error:
        return None

# Ottieni la migliore risoluzione e refresh rate
def get_highest_resolution_and_refresh_rate():
    device_name = win32api.EnumDisplayDevices(None, 0).DeviceName
    best_mode = None
    max_resolution = (0, 0)
    max_refresh_rate = 0

    i = 0
    while True:
        try:
            mode = win32api.EnumDisplaySettings(device_name, i)
            resolution = (mode.PelsWidth, mode.PelsHeight)
            refresh_rate = mode.DisplayFrequency

            if resolution > max_resolution or (resolution == max_resolution and refresh_rate > max_refresh_rate):
                max_resolution = resolution
                max_refresh_rate = refresh_rate
                best_mode = mode

            i += 1
        except pywintypes.error:
            break
    
    return best_mode

# Funzione per cambiare la risoluzione e il refresh rate usando QRes
def change_display_settings_with_qres(qres_executable, width, height, refresh_rate):
    # Costruisce il comando per QRes
    command = f'"{qres_executable}" /x:{width} /y:{height} /r:{refresh_rate}'
    
    # Stampa il comando per il debugging
    print(f"Eseguo il comando: {command}")
    
    # Esegue il comando
    result = subprocess.run(command, shell=True)
    
    if result.returncode == 0:
        print(f"Risoluzione cambiata con successo a: {width}x{height}, {refresh_rate}Hz")
    else:
        print("Errore nel cambiare la risoluzione con QRes.")

if __name__ == "__main__":
    # Estrai il file ZIP e ottieni la directory temporanea
    temp_dir = extract_zip_to_temp()
    
    # Percorso del file QRes.exe estratto
    qres_executable = os.path.join(temp_dir, "QRes.exe")

    # Ottieni la risoluzione e il refresh rate attuali
    current_resolution, current_refresh_rate = get_current_resolution_and_refresh_rate()
    if current_resolution and current_refresh_rate:
        print(f"Risoluzione attuale: {current_resolution[0]}x{current_resolution[1]}, Frequenza: {current_refresh_rate}Hz")
    else:
        print("Impossibile ottenere la risoluzione attuale.")

    # Ottieni la migliore risoluzione e refresh rate disponibili
    best_mode = get_highest_resolution_and_refresh_rate()
    if best_mode:
        print(f"Imposto la migliore risoluzione: {best_mode.PelsWidth}x{best_mode.PelsHeight}, Frequenza: {best_mode.DisplayFrequency}Hz")
        change_display_settings_with_qres(qres_executable, best_mode.PelsWidth, best_mode.PelsHeight, best_mode.DisplayFrequency)
    else:
        print("Nessuna modalità trovata.")
    
    # Pulisci la directory temporanea
    shutil.rmtree(temp_dir)
    time.sleep(2)
