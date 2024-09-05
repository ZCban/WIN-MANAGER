import subprocess
import os
import shutil
import time

def run_powershell_command(command):
    """Esegue un comando PowerShell e ritorna l'output."""
    result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    return result.stdout, result.stderr

def install_pswindowsupdate():
    print("Installazione del PackageProvider NuGet...")
    try:
        stdout, stderr = run_powershell_command('Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force')
        print("NuGet installato correttamente.")
    except Exception as e:
        print(f"Errore durante l'installazione di NuGet: {e}")
    
    print("Installazione del modulo PSWindowsUpdate...")
    try:
        stdout, stderr = run_powershell_command("Install-Module -Name PSWindowsUpdate -Force")
        print("PSWindowsUpdate installato correttamente.")
        return stdout, stderr  # Restituisci i valori per l'uso successivo
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'installazione di PSWindowsUpdate: {e}")
        print(e.stdout)
        print(e.stderr)
        return e.stdout, e.stderr  # Restituisci gli errori catturati


def check_pswindowsupdate_installed():
    """Verifica se il modulo PSWindowsUpdate è stato installato."""
    check_command = "Get-Module -ListAvailable -Name PSWindowsUpdate"
    stdout, stderr = run_powershell_command(check_command)
    return "PSWindowsUpdate" in stdout

def clear_windows_update_cache():
    """Cancella la cache di Windows Update."""
    # Arresta il servizio Windows Update
    stop_service_command = "Stop-Service -Name wuauserv -Force"
    run_powershell_command(stop_service_command)

    # Cancella il contenuto della cartella SoftwareDistribution
    cache_dir = r"C:\Windows\SoftwareDistribution"
    if os.path.exists(cache_dir):
        # Usa shutil.rmtree per rimuovere l'intera directory
        shutil.rmtree(cache_dir)
        # Ricrea la directory vuota
        os.makedirs(cache_dir)

    # Avvia il servizio Windows Update
    start_service_command = "Start-Service -Name wuauserv"
    run_powershell_command(start_service_command)

    print("Cache di Windows Update cancellata.")

def get_windows_updates():
    """Ottiene la lista degli aggiornamenti disponibili."""
    command = "Get-WindowsUpdate"
    stdout, stderr = run_powershell_command(command)
    if stderr:
        print("Errore durante l'esecuzione di Get-WindowsUpdate:", stderr)
        return None
    return stdout

def install_windows_updates():
    """Installa tutti gli aggiornamenti disponibili e riavvia automaticamente se necessario."""
    command = "Get-WindowsUpdate -AcceptAll -Install -AutoReboot"
    stdout, stderr = run_powershell_command(command)
    if stderr:
        print("Errore durante l'installazione degli aggiornamenti:", stderr)
        return None
    return stdout

def auto_up():
    # Passi dello script
    print("Installazione del modulo PSWindowsUpdate...")
    stdout, stderr = install_pswindowsupdate()
    if stderr:
        print("Errore durante l'installazione del modulo PSWindowsUpdate:", stderr)
    print("Verifica dell'installazione del modulo...")
    if check_pswindowsupdate_installed():
        print("Il modulo PSWindowsUpdate è stato installato correttamente.")
    print("Cancellazione della cache di Windows Update...")
    clear_windows_update_cache()
    time.sleep(0.5)  # Attendi qualche secondo per assicurarti che il servizio sia avviato correttamente
    print("Controllo degli aggiornamenti di Windows...")
    updates = get_windows_updates()
    if updates and "No updates are available" not in updates:
        print("Aggiornamenti disponibili:\n", updates)
        print("Installazione degli aggiornamenti...")
        update_result = install_windows_updates()
        
        if update_result:
            print("Risultato installazione aggiornamenti:\n", update_result)
    else:
        print("Nessun aggiornamento disponibile.")


