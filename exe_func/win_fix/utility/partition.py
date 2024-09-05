import subprocess

def run_diskpart(commands):
    """
    Esegue una lista di comandi diskpart.
    """
    script = "\n".join(commands)
    process = subprocess.run(["diskpart"], input=script, text=True, capture_output=True)
    if process.returncode != 0:
        raise Exception(f"Errore durante l'esecuzione di diskpart: {process.stderr}")
    return process.stdout

def get_efi_partition_number():
    try:
        # Seleziona il disco 0 e lista tutte le partizioni
        output = run_diskpart([
            "select disk 0",
            "list partition"
        ])
        
        lines = output.splitlines()

        # Cerca la partizione con il tipo "System" o "Sistema"
        for line in lines:
            if "System" in line or "Sistema" in line:  # Cerca entrambe le parole chiave
                parts = line.split()
                return parts[1]  # Si presume che il numero della partizione sia nella seconda colonna
    except Exception as e:
        print(f"Errore durante l'identificazione della partizione EFI: {e}")
    return None

def assign_letter_to_efi_partition(partition_number):
    try:
        # Assegna una lettera alla partizione EFI usando diskpart
        run_diskpart([
            "select disk 0",
            f"select partition {partition_number}",
            "assign letter=Z"
        ])
    except Exception as e:
        print(f"Errore durante l'assegnazione della lettera alla partizione EFI: {e}")

def remove_letter_from_efi_partition(partition_number):
    try:
        # Rimuove la lettera dalla partizione EFI
        run_diskpart([
            "select disk 0",
            f"select partition {partition_number}",
            "remove letter=Z"
        ])
    except Exception as e:
        print(f"Errore durante la rimozione della lettera dalla partizione EFI: {e}")

def rebuild_uefi_bootloader():
    try:
        # Ricostruisce il bootloader UEFI
        run_command("bcdboot C:\\Windows /s Z: /f UEFI")
    except Exception as e:
        print(f"Errore durante la ricostruzione del bootloader UEFI: {e}")

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione del comando {command}: {e}")

if __name__ == "__main__":
    partition_number = get_efi_partition_number()
    if partition_number:
        assign_letter_to_efi_partition(partition_number)
        rebuild_uefi_bootloader()
        remove_letter_from_efi_partition(partition_number)
    else:
        print("Impossibile trovare la partizione EFI.")

