import subprocess
import time
import os
import shutil


def run_powershell_command(command, capture_output=True):
    """Esegue un comando PowerShell e ritorna l'output."""
    try:
        completed_process = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=capture_output, text=True, check=True
        )
        if capture_output:
            print(completed_process.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione del comando: {e}")
        if capture_output:
            print(e.stdout)
            print(e.stderr)

def disinstalla_versione_precedente_DesktopAppInstaller():
    print("Disinstallazione delle versioni precedenti del pacchetto DesktopAppInstaller")
    run_powershell_command('Get-AppxPackage -Name "Microsoft.DesktopAppInstaller" | Remove-AppxPackage')

def ripristina_windows_store():
    print("Reset di Microsoft Store...")
    run_powershell_command('wsreset.exe', capture_output=False)
    time.sleep(1)  # Attende che lo Store si apra completamente
    print("Chiusura di Microsoft Store...")
    run_powershell_command('Stop-Process -Name "WinStore.App" -Force')
    print("Pulizia della cache del Microsoft Store...")
    cache_path = os.path.expandvars(r"%localappdata%\Packages\Microsoft.WindowsStore_8wekyb3d8bbwe\LocalCache")
    
    if os.path.exists(cache_path):
        try:
            shutil.rmtree(cache_path)
            print(f"Cache del Microsoft Store rimossa: {cache_path}")
        except Exception as e:
            print(f"Errore durante la rimozione della cache: {e}")
    else:
        print(f"La cartella di cache non esiste")


def ripristina_AppXManifest_app_predefinite():
    print("Ripristino AppXManifest delle app predefinite...")
    run_powershell_command('Get-AppxPackage | foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\\AppXManifest.xml"}')

def esegui_sfc():
    print("Esecuzione di SFC (System File Checker)...")
    try:
        subprocess.run(
            ["powershell", "-Command", "sfc /scannow"],
            check=True
        )
        print('completato')
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione del comando SFC: {e}")


def usa_dism():
    print("Utilizzo di DISM CheckHealth per riparare l'immagine del sistema...")
    try:
        subprocess.run(
            ["powershell", "-Command", "DISM /Online /Cleanup-Image /CheckHealth"],
            check=True
        )
        print('completato')
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione del comando DISM: {e}")
        
    print("Utilizzo di DISM ScanHealth per riparare l'immagine del sistema...")
    try:
        subprocess.run(
            ["powershell", "-Command", "DISM /Online /Cleanup-Image /ScanHealth"],
            check=True
        )
        print('completato')
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione del comando DISM: {e}")

    print("Utilizzo di DISM RestoreHealth per riparare l'immagine del sistema...")
    try:
        subprocess.run(
            ["powershell", "-Command", "DISM /Online /Cleanup-Image /RestoreHealth"],
            check=True
        )
        print('completato')
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione del comando DISM: {e}")

    print("Utilizzo di DISM StartComponentCleanup per riparare l'immagine del sistema...")
    try:
        subprocess.run(
            ["powershell", "-Command", "DISM /Online /Cleanup-Image /StartComponentCleanup"],
            check=True
        )
        print('completato')
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione del comando DISM: {e}")

    print("Utilizzo di DISM analyzecomponentstore per riparare l'immagine del sistema...")
    try:
        subprocess.run(
            ["powershell", "-Command", "DISM /Online /Cleanup-Image /analyzecomponentstore"],
            check=True
        )
        print('completato')
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione del comando DISM: {e}")

def check_disks_and_run_chkdsk():
    print("Verifica dei dischi e esecuzione di chkdsk...")
    try:
        # Lista tutti i drive con DriveType=3 (hard disk)
        result = subprocess.run("wmic logicaldisk where \"DriveType=3\" get DeviceID", check=True, shell=True, capture_output=True, text=True)
        drives = result.stdout.split()
        for drive in drives:
            if drive and drive != 'C:':  # Evita l'unità C: per l'ultimo step
                print(f"Eseguendo chkdsk su {drive}...")
                run_powershell_command(f"chkdsk {drive} /f")

        # Esegui chkdsk su C: come ultimo passo
        print("Eseguendo chkdsk su C: per ultimo...")
        # Forza la risposta 'Y' per confermare l'esecuzione di chkdsk al riavvio
        run_powershell_command("echo Y | chkdsk C: /f")
    except Exception as e:
        print(f"Errore durante l'esecuzione di chkdsk: {e}")

def reset_network_settings():
    print("Rilascio dell'indirizzo IP...")
    run_powershell_command('ipconfig /release')
    
    print("Rinnovo dell'indirizzo IP...")
    run_powershell_command('ipconfig /renew')
    
    print("Svuotamento della cache DNS...")
    run_powershell_command('ipconfig /flushdns')
    
    print("Reset del catalogo Winsock...")
    run_powershell_command('netsh winsock reset')
    
    print("Reset della configurazione IP...")
    run_powershell_command('netsh int ip reset')
    
    print("Reset della configurazione del firewall di Windows...")
    run_powershell_command('netsh advfirewall reset')


def rebuild_bcd():
    """
    Ricostruzione del Boot Configuration Data (BCD) su Sistemi GPT/UEFI
    """
    try:
        subprocess.run(['bootrec', '/rebuildbcd'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Errore durante la ricostruzione del BCD: {e}")


def rebuild_uefi_bootloader():
    """
    Identifica la partizione EFI, assegna una lettera di unità, ricostruisce il bootloader UEFI e poi rimuove la lettera di unità.
    """
    def run_diskpart(commands):
        script = "\n".join(commands)
        process = subprocess.run(["diskpart"], input=script, text=True, capture_output=True)
        if process.returncode != 0:
            raise Exception(f"Errore durante l'esecuzione di diskpart: {process.stderr}")
        return process.stdout

    def run_command(command):
        try:
            subprocess.run(command, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Errore durante l'esecuzione del comando {command}: {e}")

    try:
        # Seleziona il disco 0 e lista tutte le partizioni
        output = run_diskpart([
            "select disk 0",
            "list partition"
        ])
        
        lines = output.splitlines()

        # Cerca la partizione con il tipo "System" o "Sistema"
        partition_number = None
        for line in lines:
            if "System" in line or "Sistema" in line:
                parts = line.split()
                partition_number = parts[1]  # Si presume che il numero della partizione sia nella seconda colonna
                break
        
        if not partition_number:
            print("Impossibile trovare la partizione EFI.")
            return

        # Assegna una lettera alla partizione EFI
        run_diskpart([
            "select disk 0",
            f"select partition {partition_number}",
            "assign letter=Z"
        ])
        
        # Ricostruisce il bootloader UEFI
        run_command("bcdboot C:\\Windows /s Z: /f UEFI")
        
        # Rimuove la lettera dalla partizione EFI
        run_diskpart([
            "select disk 0",
            f"select partition {partition_number}",
            "remove letter=Z"
        ])
        
        print("Bootloader UEFI ricostruito con successo.")
    
    except Exception as e:
        print(f"Errore durante il processo: {e}")


def esegui_ripristino():
    print("Inizio delle operazioni di manutenzione del sistema...")

    # Disinstallazione delle versioni precedenti di DesktopAppInstaller
    disinstalla_versione_precedente_DesktopAppInstaller()

    # Ripristino di Microsoft Store
    ripristina_windows_store()

    # Ripristino AppXManifest delle app predefinite
    ripristina_AppXManifest_app_predefinite()

    # Esecuzione di SFC
    esegui_sfc()

    # Utilizzo di DISM per riparare l'immagine del sistema
    usa_dism()

    # Verifica dei dischi e esecuzione di chkdsk
    check_disks_and_run_chkdsk()

    # Reset delle impostazioni di rete
    reset_network_settings()

    print("Operazioni di manutenzione completate.")
