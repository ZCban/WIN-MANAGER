import subprocess
import re

def compare_versions(version1, version2):
    """Confronta due versioni del driver nel formato 'xx.xx.xx.xxxx'."""
    # Dividi le versioni in liste di interi per poterle confrontare
    version1_parts = list(map(int, version1.split('.')))
    version2_parts = list(map(int, version2.split('.')))
    
    # Confronta le versioni parte per parte
    return version1_parts < version2_parts

def get_gpu_info():
    try:
        # Usa PowerShell per ottenere nome, versione del driver e fornitore del driver
        ps_command = (
            "Get-WmiObject Win32_PnPSignedDriver | "
            "Where-Object { $_.DeviceClass -eq 'DISPLAY' } | "
            "Select-Object DeviceName, DriverVersion, Manufacturer | Format-Table -HideTableHeaders"
        )
        result = subprocess.check_output(["powershell", "-Command", ps_command], shell=True)
        
        # Decodifica il risultato e dividi in righe
        result_str = result.decode().strip().split("\n")
        
        # Rimuovi eventuali righe vuote
        cleaned_result = [line.strip() for line in result_str if line.strip()]
        
        # Ora cleaned_result dovrebbe contenere solo i dati, senza intestazioni
        if len(cleaned_result) >= 1:
            # Supponiamo che la versione del driver contenga numeri e punti, usiamo regex per trovarla
            pattern = r"(\d+\.\d+\.\d+\.\d+)"  # Match per qualcosa come 32.0.15.6081
            
            # Cerchiamo di trovare la versione del driver
            match = re.search(pattern, cleaned_result[0])
            
            if match:
                driver_version = match.group(1)  # La versione del driver
                
                # Il nome della scheda grafica è tutto ciò che precede la versione del driver
                name_and_manufacturer = cleaned_result[0][:match.start()].strip()
                
                # Il fornitore del driver è tutto ciò che segue la versione del driver
                manufacturer = cleaned_result[0][match.end():].strip()
                
                return name_and_manufacturer, driver_version, manufacturer
            else:
                return None, None, "Impossibile trovare la versione del driver"
        else:
            return None, None, "Nessun dato disponibile"
    
    except Exception as e:
        return None, None, f"Errore nel recuperare le informazioni: {e}"

# Funzione principale
def nvidia():
    # Versione del driver di riferimento per il confronto
    versione_riferimento = "31.0.15.3161"
    
    # Ottieni le informazioni sulla GPU
    gpu_name, driver_version, driver_provider = get_gpu_info()

    if gpu_name and driver_version and driver_provider:
        print(f"Nome della scheda grafica: {gpu_name}")
        print(f"Versione del driver: {driver_version}")
        print(f"Fornitore del driver: {driver_provider}")
        
        # Controlla se la versione del driver è inferiore alla versione di riferimento
        if compare_versions(driver_version, versione_riferimento) or "Microsoft" in driver_provider:
            print("Si consiglia di aggiornare il driver della scheda grafica.")
        else:
            print("Il driver della scheda grafica è abbastanza recente.")
    else:
        print(driver_provider)  # Se c'è un errore, viene stampato qui

# Esegui il codice principale
nvidia()

