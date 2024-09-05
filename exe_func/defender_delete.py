import os
import subprocess
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    # Ottieni il percorso dello script Python attualmente in esecuzione
    script_path = os.path.abspath(__file__)

    # Crea un file batch temporaneo
    bat_path = os.path.join(os.getenv("TEMP"), "run_as_admin.bat")
    with open(bat_path, 'w') as bat_file:
        bat_file.write(f'@echo off\n')
        bat_file.write(f'python "{script_path}"\n')  # Comando per eseguire lo script Python corrente
        bat_file.write('exit\n')

    # Usa ctypes per eseguire il file batch con privilegi di amministratore
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f'/c "{bat_path}"', None, 1)
    except Exception as e:
        print(f"Errore nell'esecuzione come amministratore: {e}")
        sys.exit(1)

def import_reg_files(folder_path):
    # Verifica che la cartella esista
    if not os.path.exists(folder_path):
        print(f"La cartella '{folder_path}' non esiste.")
        return

    # Elenco di tutti i file .reg presenti nella cartella
    reg_files = [f for f in os.listdir(folder_path) if f.endswith('.reg')]

    # Verifica se ci sono file .reg nella cartella
    if not reg_files:
        print("Nessun file .reg trovato nella cartella.")
        return

    # Importa ogni file .reg
    for reg_file in reg_files:
        reg_file_path = os.path.join(folder_path, reg_file)
        print(f"Importando il file: {reg_file_path}")
        
        try:
            # Comando per importare il file .reg come amministratore
            subprocess.run(["reg", "import", reg_file_path], check=True)
            print(f"File {reg_file} importato con successo.")
        except subprocess.CalledProcessError as e:
            print(f"Errore durante l'importazione del file {reg_file}: {e}")

    print("Operazione completata.")

def Remove_defender():
    if is_admin():
        import_reg_files("Remove_defender")
    else:
        print("Il programma richiede i privilegi di amministratore per funzionare correttamente. Tentativo di riavvio come amministratore...")
        run_as_admin()


