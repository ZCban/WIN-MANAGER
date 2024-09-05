import subprocess
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Lista unica delle applicazioni disponibili
apps = [
    ('7-Zip', '7zip.7zip'),
    ('Git', 'Git.Git'),
    ('MSI Afterburner', 'Guru3D.Afterburner'),
    ('GPU-Z', 'TechPowerUp.GPU-Z'),
    ('DDU (Display Driver Uninstaller)', 'Wagnardsoft.DisplayDriverUninstaller'),
    ('CPU-Z', 'CPUID.CPU-Z'),
    ('HxD Hex Editor', 'MHNexus.HxD'),
    ('Arduino IDE', 'ArduinoSA.IDE.stable'),
    ('Visual Studio 2022 Community', 'Microsoft.VisualStudio.2022.Community'),
    ('Brave Browser', 'Brave.Brave'),
    ('Google Chrome', 'Google.Chrome'),
    ('Mozilla Firefox', 'Mozilla.Firefox'),
    ('Opera Browser', 'Opera.Opera'),
    ('Microsoft Edge', 'Microsoft.Edge'),
    ('Python 3.9', 'Python.Python.3.9'),
    ('Python 3.10', 'Python.Python.3.10'),
    ('Python 3.11', 'Python.Python.3.11'),
    ('Python 3.12', 'Python.Python.3.12'),
    ('Chocolatey', 'Chocolatey.Chocolatey'),
    ('NordVPN', 'NordSecurity.NordVPN'),
    ('Discord', 'Discord.Discord'),
    ('WhatsApp', 'WhatsApp.WhatsApp'),
    ('Telegram Desktop', 'Telegram.TelegramDesktop'),
    ('Skype', 'Microsoft.Skype'),
    ('Steam', 'Valve.Steam'),
    ('Ubisoft Connect', 'Ubisoft.Connect'),
    ('Epic Games Launcher', 'EpicGames.EpicGamesLauncher'),
    ('Valorant', 'RiotGames.Valorant.EU'),
    ('EA Desktop', 'ElectronicArts.EADesktop'),
    ('Nvidia GeForce Now', 'Nvidia.GeForceNow'),
    ('Spotify', 'Spotify.Spotify'),
    ('YouTube Music Desktop', 'Ytmdesktop.Ytmdesktop'),
    ('VLC Media Player', 'VideoLAN.VLC'),
    ('iTunes', 'Apple.iTunes'),
    ('OBS Studio', 'OBSProject.OBSStudio'),
    ('AnyDesk', 'AnyDeskSoftwareGmbH.AnyDesk'),
    ('TeamViewer', 'TeamViewer.TeamViewer'),
    ('Logitech Gaming Software', 'Logitech.LGS'),
    ('Microsoft Office', 'Microsoft.Office'),
    ('OpenOffice', 'Apache.OpenOffice'),
    ('LibreOffice', 'TheDocumentFoundation.LibreOffice'),
    ('Nvidia GeForce Experience', 'Nvidia.GeForceExperience'),
    ('Nvidia CUDA', 'Nvidia.CUDA'),
    ('Mozilla Thunderbird', 'Mozilla.Thunderbird')
]

# Funzione per eseguire comandi PowerShell e catturare output in tempo reale
def run_powershell_command(command, output_callback):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        output = process.stdout.readline()
        if output:
            output_callback(output.strip() + "\n")
        if process.poll() is not None:
            break
    rc = process.poll()
    return rc

def start_installation(selected_apps, terminal_insert):
    terminal_insert("Inizio installazione...\n")
    for app in selected_apps:
        command = f"winget install {app} -e --accept-source-agreements"
        run_powershell_command(command, terminal_insert)
    terminal_insert("Installazione completata!\n")

def start_uninstallation(selected_apps, terminal_insert):
    terminal_insert("Inizio disinstallazione...\n")
    for app in selected_apps:
        command = f"powershell -Command \"winget uninstall {app} -e --accept-source-agreements -h\""
        run_powershell_command(command, terminal_insert)
    terminal_insert("Disinstallazione completata!\n")

def update_all_apps(terminal_insert):
    try:
        # Esegui il comando 'winget upgrade --all' per aggiornare tutti i pacchetti disponibili
        process = subprocess.Popen(
            ['winget', 'upgrade', '--all','--include-unknown', '--accept-package-agreements', '--accept-source-agreements'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Leggi l'output riga per riga e stampalo in tempo reale
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        # Controlla se il processo ha restituito un codice di errore
        rc = process.poll()
        if rc == 0:
            print("Tutti i pacchetti aggiornabili sono stati aggiornati con successo.")
        else:
            print(f"Errore durante l'aggiornamento dei pacchetti. Codice di ritorno: {rc}")
    except FileNotFoundError:
        print("Il comando 'winget' non è stato trovato. Assicurati che Winget sia installato sul tuo sistema.")

def start_user_installation(app_vars, terminal_insert):
    selected_apps = [app_id for app_id, var in app_vars.items() if var.get()]
    if not selected_apps:
        messagebox.showwarning("Nessuna selezione", "Seleziona almeno un'applicazione da installare.")
        return
    threading.Thread(target=start_installation, args=(selected_apps, terminal_insert)).start()

def start_user_uninstallation(app_vars, terminal_insert):
    selected_apps = [app_id for app_id, var in app_vars.items() if var.get()]
    if not selected_apps:
        messagebox.showwarning("Nessuna selezione", "Seleziona almeno un'applicazione da disinstallare.")
        return
    threading.Thread(target=start_uninstallation, args=(selected_apps, terminal_insert)).start()

def user_update_all_apps(terminal_insert):
    threading.Thread(target=update_all_apps, args=(terminal_insert,)).start()

