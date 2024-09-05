import os
import glob
import shutil
import subprocess
import ctypes
import json
from ctypes import wintypes
import time
import threading
import concurrent.futures


def svuota_d3dscache():
    percorso_cache = os.path.join(os.getenv('LOCALAPPDATA'), 'D3DSCache')
    
    if os.path.exists(percorso_cache):
        for elemento in os.listdir(percorso_cache):
            percorso_elemento = os.path.join(percorso_cache, elemento)
            try:
                if os.path.isfile(percorso_elemento) or os.path.islink(percorso_elemento):
                    os.unlink(percorso_elemento)
                elif os.path.isdir(percorso_elemento):
                    shutil.rmtree(percorso_elemento)
            except Exception as e:
                print(f"Errore durante la rimozione di {percorso_elemento}: {e}")
        print(f"La cartella {percorso_cache} è stata svuotata con successo.")
    else:
        print(f"La cartella {percorso_cache} non esiste.")

def clear_event_logs():
    logs_to_clear = ['System', 'Security', 'Application']
    
    for log in logs_to_clear:
        try:
            command = ['wevtutil', 'cl', log]
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Successfully cleared {log} log.")
        except subprocess.CalledProcessError as e:
            print(f"Error clearing {log} log: {e.stderr}")

def delete_thumbcache_files(directory):
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.startswith('thumbcache'):
                file_path = os.path.join(root, filename)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except FileNotFoundError:
                    print(f"File not found: {file_path}")
                except PermissionError:
                    print(f"Permission denied: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

def delete_wer_files():
    wer_path = r'C:\ProgramData\Microsoft\Windows\WER'

    if os.path.exists(wer_path):
        for root, dirs, files in os.walk(wer_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f'Eliminato: {file_path}')
                except Exception as e:
                    print(f'Errore nell\'eliminazione di {file_path}: {e}')
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    os.rmdir(dir_path)
                    print(f'Eliminata cartella: {dir_path}')
                except Exception as e:
                    print(f'Errore nell\'eliminazione della cartella {dir_path}: {e}')

        try:
            os.system('rd /s /q %systemdrive%\\$Recycle.Bin')
            print('Cestino svuotato.')
        except Exception as e:
            print(f'Errore nello svuotamento del Cestino: {e}')
    else:
        print(f'La cartella WER non esiste al percorso {wer_path}')

def clear_cryptnet_url_cache():
    directory = os.path.expandvars(r'%LocalAppData%\..\LocalLow\Microsoft\CryptnetUrlCache')

    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    os.unlink(file_path)
                    print(f'Eliminato: {file_path}')
                except Exception as e:
                    print(f'Errore durante l\'eliminazione del file {file_path}. Eccezione: {e}')
            for name in dirs:
                dir_path = os.path.join(root, name)
                try:
                    shutil.rmtree(dir_path)
                    print(f'Eliminata directory: {dir_path}')
                except Exception as e:
                    print(f'Errore durante l\'eliminazione della directory {dir_path}. Eccezione: {e}')
        print(f'Pulizia della CryptnetUrlCache completata.')
    else:
        print(f'La directory {directory} non esiste')

def clean_windows_temp():
    directory = r'C:\Windows\Temp'

    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Errore durante l\'eliminazione del file {file_path}. Eccezione: {e}')
        print('Pulizia di C:\\Windows\\Temp completata.')
    else:
        print(f'La directory {directory} non esiste')

def pulisci_file_recenti():
    percorso_recenti = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Recent')

    if os.path.exists(percorso_recenti):
        for file_name in os.listdir(percorso_recenti):
            file_path = os.path.join(percorso_recenti, file_name)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                    print(f'File eliminato: {file_path}')
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f'Directory eliminata: {file_path}')
            except Exception as e:
                print(f'Errore durante l\'eliminazione di {file_path}: {e}')
    else:
        print(f'La directory {percorso_recenti} non esiste o non è accessibile.')

def clean_programs_error_report():
    directory = os.path.expandvars(r'%LOCALAPPDATA%\ElevatedDiagnostics')

    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print(f'Eliminato: {file_path}')
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f'Eliminata directory: {file_path}')
            except PermissionError as e:
                print(f'Accesso negato durante l\'eliminazione del file {file_path}. Eccezione: {e}')
            except Exception as e:
                print(f'Errore durante l\'eliminazione del file {file_path}. Eccezione: {e}')
        print('Pulizia della directory Programs Error Report completata.')
    else:
        print(f'La directory {directory} non esiste')


def trova_file(directory_di_partenza='C:\\', estensioni=None):
    if estensioni is None:
        estensioni = ['.log', '.LOG2', '.LOG1', '.etl', '.evt', '.evtx', '.dmp']
    
    file_da_eliminare = []

    print(f"Ricerca dei file nella directory {directory_di_partenza} con le estensioni {estensioni}...")

    # Trova tutti i file con le estensioni specificate nella directory e nelle sottodirectory
    for root, dirs, files in os.walk(directory_di_partenza):
        for file in files:
            if any(file.lower().endswith(ext.lower()) for ext in estensioni):
                file_da_eliminare.append(os.path.join(root, file))
    
    print(f"Trovati {len(file_da_eliminare)} file da eliminare.")
    return file_da_eliminare

def elimina_file(file):
    try:
        os.remove(file)
        print(f'File eliminato: {file}')
    except Exception as e:
        print(f'Errore durante l\'eliminazione di {file}: {e}')

def clean_log_files(start_directory='C:\\'):
    estensioni = ['.log', '.LOG2', '.LOG1', '.etl', '.evt', '.evtx', '.dmp']
    file_da_eliminare = trova_file(start_directory, estensioni)
    
    if file_da_eliminare:
        print("Inizio eliminazione dei file...")
        # Utilizza il multithreading per eliminare i file in parallelo
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(elimina_file, file_da_eliminare)
        print("Eliminazione completata.")
    else:
        print("Nessun file da eliminare.")


def clean_user_temp():
    # Specifica il percorso della directory temporanea dell'utente
    directory = os.path.expandvars(r'%TEMP%')

    # Verifica se la directory esiste
    if os.path.exists(directory):
        # Elimina tutti i file e le sottocartelle nella directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Elimina il file
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Elimina la directory e tutto il suo contenuto
            except Exception as e:
                if "[WinError 32]" in str(e):
                    print(f'Non elimino, serve al sistema o è in uso: {file_path}')
                else:
                    print(f'Errore durante l\'eliminazione del file {file_path}. Eccezione: {e}')
        print('Pulizia della directory temporanea dell\'utente completata.')
    else:
        print(f'La directory {directory} non esiste')

def clear_discord_caches():
    """
    Elimina le cache di Discord.
    """
    # Percorsi delle cache di Discord
    cache_directories = [
        os.path.expandvars(r'%AppData%\Discord\Cache'),
        os.path.expandvars(r'%AppData%\Discord\Code Cache'),
        os.path.expandvars(r'%AppData%\Discord\GPUCache'),
    ]

    for directory in cache_directories:
        print(f'Pulizia della cache di Discord: {directory}')
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Errore durante l\'eliminazione del file {file_path}. Eccezione: {e}')
            print(f'Pulizia della directory {directory} completata.')
        else:
            print(f'La directory {directory} non esiste')


def clear_amd_cache():
    # Ottieni il percorso della directory principale dell'utente corrente
    user_home = os.path.expanduser('~')
    base_cache_path = os.path.join(user_home, "AppData", "Local", "AMD")

    # Percorsi della cache
    dx_cache_path = os.path.join(base_cache_path, "DxCache")
    ogl_cache_path = os.path.join(base_cache_path, "OglCache")
    vk_cache_path = os.path.join(base_cache_path, "VkCache")

    # Funzione per cancellare i file all'interno di una cartella
    def clear_cache(cache_path):
        if os.path.exists(cache_path):
            for root, dirs, files in os.walk(cache_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        print(f"File rimosso: {file_path}")
                    except Exception as e:
                        print(f"Errore nella rimozione forse serve a sistema {file_path}")
        else:
            print(f"La cartella {cache_path} non esiste")

    # Cancella le cache
    clear_cache(dx_cache_path)
    clear_cache(ogl_cache_path)
    clear_cache(vk_cache_path)

def clear_nvidia_cache():
    # Specifica il percorso della directory da svuotare
    directory = os.path.expandvars(r'%AppData%\..\LocalLow\NVIDIA\PerDriverVersion\DXCache')

    # Verifica se la directory esiste
    if os.path.exists(directory):
        # Elimina tutti i file e le sottocartelle nella directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Elimina il file
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Elimina la directory e tutto il suo contenuto
            except Exception as e:
                if "[WinError 32]" in str(e):
                    print(f'Non elimino, serve al sistema: {file_path}')
                else:
                    print(f'Errore durante l\'eliminazione del file {file_path}. Eccezione: {e}')
        print('Pulizia dxcache completata.')
    else:
        print(f'La directory {directory} non esiste')

    # Specifica il percorso della directory da svuotare
    directory = os.path.expandvars(r'%AppData%\..\Local\NVIDIA\GLCache')

    # Verifica se la directory esiste
    if os.path.exists(directory):
        # Elimina tutti i file e le sottocartelle nella directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Elimina il file
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Elimina la directory e tutto il suo contenuto
            except Exception as e:
                print(f'Errore durante l\'eliminazione del file {file_path}. Eccezione: {e}')
        print('Pulizia glcache completata.')
    else:
        print(f'La directory {directory} non esiste')

def clean_integrated_intel():
    # Cache degli shader Intel
    intel_cache_dirs = [
        os.path.expandvars(r'%LocalAppData%\..\LocalLow\Intel\ShaderCache'),
        os.path.expandvars(r'%LocalAppData%\..\LocalLow\Intel\DxCache')
    ]
    for directory in intel_cache_dirs:
        print(f'Pulizia della cache degli shader Intel: {directory}')
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Errore durante l\'eliminazione del file {file_path}. Eccezione: {e}')
            print(f'Pulizia della directory {directory} completata.')
        else:
            print(f'La directory {directory} non esiste')

def clean_integrated_amd():
    # Cache degli shader AMD
    amd_cache_dirs = [
        os.path.expandvars(r'%LocalAppData%\AMD\DxCache'),
        os.path.expandvars(r'%LocalAppData%\AMD\GLCache')
    ]
    for directory in amd_cache_dirs:
        print(f'Pulizia della cache degli shader AMD: {directory}')
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Errore durante l\'eliminazione del file {file_path}. Eccezione: {e}')
            print(f'Pulizia della directory {directory} completata.')
        else:
            print(f'La directory {directory} non esiste')




class ServiceManager:
    BATCH_FILE_PATH = "clean_system.bat"
    
    @staticmethod
    def is_admin():
        """Check if the script is running with administrative privileges."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    @staticmethod
    def create_batch_file(commands):
        """Create a batch file with the given commands."""
        with open(ServiceManager.BATCH_FILE_PATH, 'w') as batch_file:
            batch_file.write("@echo off\n")
            for command, description in commands:
                batch_file.write(f"echo {description}\n")
                batch_file.write(f"{command}\n")
            batch_file.write("exit\n")  # Optional: Pause at the end to see the results

    @staticmethod
    def run_batch_file_as_admin():
        """Run the batch file with administrative privileges."""
        if ServiceManager.is_admin():
            print(f"Executing batch file: {ServiceManager.BATCH_FILE_PATH}")
            subprocess.run(f'start /wait "" "{ServiceManager.BATCH_FILE_PATH}"', shell=True)
        else:
            # Run the batch file as an administrator
            try:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", ServiceManager.BATCH_FILE_PATH, None, None, 1)
            except Exception as e:
                print(f"Failed to run the batch file as admin: {e}")

    @staticmethod
    def clean_system_files():
        """Generate and execute a batch file to perform various system cleaning tasks."""
        commands = [
            ("cleanmgr /sagerun:1", "Clean temporary system files"),
            ("del /q /f /s %temp%\\*", "Clean Windows temporary files"),
            ("del /q /f /s %systemroot%\\Logs\\*", "Clean Windows log files"),
            ("del /q /f /s %systemroot%\\Panther\\*", "Clean Windows Panther logs"),
            ("ipconfig /flushdns", "Flush DNS cache"),
            ("netsh interface ip delete arpcache", "Delete ARP cache"),
            ("netsh winsock reset", "Reset Winsock"),
            ("del /q /f /s %systemroot%\\Minidump\\*", "Clean Windows Minidump"),
            ("WEvtUtil cl Application", "Clear Windows Event Logs - Application"),
            ("Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase", "Remove obsolete installation files"),
            ("del /q /f /s %userprofile%\\Downloads\\*", "Clean Downloads folder"),
            ("rd /s /q %systemdrive%\\$Recycle.bin", "Clean Recycle Bin"),
            ("vssadmin Delete Shadows /All /Quiet", "Clean System Restore files"),
            ("Dism.exe /online /Cleanup-Image /SPSuperseded", "Clean obsolete Windows Update files"),
            ("del /q /f /s C:\\Windows\\Prefetch\\*", "Clear Prefetch files"),
            ("net stop dosvc", "Stop Delivery Optimization service"),
            ("del /q /f /s %userprofile%\\AppData\\Local\\Microsoft\\Windows\\Explorer\\thumbcache_*", "Clear Thumbnail cache"),
            ("net stop wuauserv && del /q /f /s %systemroot%\\SoftwareDistribution\\* && net start wuauserv", "Clear Windows Update cache"),
            ("sc config wsearch start=disabled && net stop wsearch", "Disable Indexing service"),
            ("netsh advfirewall reset", "Reset firewall rules"),
            #("Dism.exe /Online /Cleanup-Image /AnalyzeComponentStore /n", "Analyze Component Store"),
        ]

        # Create batch file
        ServiceManager.create_batch_file(commands)

        # Execute the batch file as an admin
        ServiceManager.run_batch_file_as_admin()




def clean_windows(terminal_insert):
    threading.Thread(target=_clean_windows, args=(terminal_insert,)).start()
            
def _clean_windows(terminal_insert):
    svuota_d3dscache()
    clear_event_logs()
    
    thumbcache_directory = 'C:\\Users\\FBposta\\AppData\\Local\\Microsoft\\Windows\\Explorer'
    delete_thumbcache_files(thumbcache_directory)
    
    delete_wer_files()
    clear_cryptnet_url_cache()
    pulisci_file_recenti()
    clean_programs_error_report()
    
    clean_log_files('C:\\')
    clear_discord_caches()

    #clean_windows_temp()
    clean_user_temp()
    clear_amd_cache()
    clear_nvidia_cache()
    clean_integrated_intel()
    clean_integrated_amd()
    ServiceManager.clean_system_files()
    #ServiceManager.clean_system_files()
    terminal_insert('########################################################\n')
    terminal_insert('Pulizia Completata\n')
    

