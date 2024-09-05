import subprocess
import re

def compare_versions(version1, version2):
    """Confronta due versioni del driver nel formato 'xx.xx.xx.xxxx'."""
    # Dividi le versioni in liste di interi per poterle confrontare
    version1_parts = list(map(int, version1.split('.')))
    version2_parts = list(map(int, version2.split('.')))
    
    # Confronta le versioni parte per parte
    return version1_parts < version2_parts

def get_cpu_info():
    try:
        # Usa PowerShell per ottenere il nome del processore
        ps_command_name = (
            "Get-WmiObject Win32_Processor | "
            "Select-Object Name | Format-Table -HideTableHeaders"
        )
        cpu_name_result = subprocess.check_output(["powershell", "-Command", ps_command_name], shell=True)
        
        # Decodifica il risultato e ottieni il nome della CPU
        cpu_name = cpu_name_result.decode().strip().split("\n")[0].strip()
        
        # Usa PowerShell per ottenere la versione del driver e il fornitore del driver della CPU
        ps_command_driver = (
            "Get-WmiObject Win32_PnPSignedDriver | "
            "Where-Object { $_.DeviceClass -eq 'PROCESSOR' } | "
            "Select-Object DriverVersion, Manufacturer | Format-Table -HideTableHeaders"
        )
        driver_result = subprocess.check_output(["powershell", "-Command", ps_command_driver], shell=True)
        
        # Decodifica il risultato e dividi in righe
        driver_result_str = driver_result.decode().strip().split("\n")
        
        # Rimuovi eventuali righe vuote
        cleaned_driver_result = [line.strip() for line in driver_result_str if line.strip()]
        
        # Ora cleaned_driver_result dovrebbe contenere solo i dati, senza intestazioni
        if len(cleaned_driver_result) >= 1:
            # Supponiamo che la versione del driver contenga numeri e punti, usiamo regex per trovarla
            pattern = r"(\d+\.\d+\.\d+\.\d+)"  # Match per qualcosa come 10.0.22621.3672
            
            # Cerchiamo di trovare la versione del driver
            match = re.search(pattern, cleaned_driver_result[0])
            
            if match:
                driver_version = match.group(1)  # La versione del driver
                
                # Il fornitore del driver è tutto ciò che segue la versione del driver
                manufacturer = cleaned_driver_result[0][match.end():].strip()
                
                return cpu_name, driver_version, manufacturer
            else:
                return cpu_name, None, "Impossibile trovare la versione del driver"
        else:
            return cpu_name, None, "Nessun dato disponibile per il driver"
    
    except Exception as e:
        return None, None, f"Errore nel recuperare le informazioni: {e}"

# Funzione principale
def main():
    # Versione del driver di riferimento per il confronto
    versione_riferimento = "10.0.22621.3672"
    
    # Ottieni le informazioni sulla CPU
    cpu_name, driver_version, driver_provider = get_cpu_info()

    if cpu_name and driver_version and driver_provider:
        print(f"Nome della CPU: {cpu_name}")
        print(f"Versione del driver: {driver_version}")
        print(f"Fornitore del driver: {driver_provider}")
        
        # Controlla se la versione del driver è inferiore alla versione di riferimento
        if compare_versions(driver_version, versione_riferimento) or "Microsoft" in driver_provider:
            print("Si consiglia di aggiornare il driver della CPU.")
        else:
            print("Il driver della CPU è abbastanza recente.")
    elif cpu_name:
        print(f"Nome della CPU: {cpu_name}")
        print(driver_provider)  # Se c'è un errore nei driver, lo stampiamo qui
    else:
        print(driver_provider)  # Se c'è un errore generale, lo stampiamo qui

# Esegui il codice principale
main()

