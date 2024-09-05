import subprocess
import os
import sys
import time
import platform
import wmi
import shutil

class DisplayDriverUninstaller:
    ddu_path = None

    @classmethod
    def is_ddu_installed(cls):
        try:
            result = subprocess.run(['winget', 'list', '--source=winget', 'Display Driver Uninstaller'], capture_output=True, text=True)
            return 'Display Driver Uninstaller' in result.stdout
        except Exception as e:
            print(f"Error checking for DDU: {e}")
            return False

    @classmethod
    def install_ddu(cls):
        try:
            subprocess.run(['winget', 'install', '--id=Wagnardsoft.DisplayDriverUninstaller'], check=True)
        except Exception as e:
            print(f"Error installing DDU: {e}")

    @classmethod
    def find_ddu_path(cls):
        default_paths = [
            r'C:\Program Files\Display Driver Uninstaller',
            r'C:\Program Files (x86)\Display Driver Uninstaller'
        ]
        for path in default_paths:
            if os.path.exists(path):
                cls.ddu_path = path
                return path
        return None

    @classmethod
    def get_gpu_info(cls):
        try:
            # Esegue il comando WMIC per ottenere informazioni sulla scheda grafica
            output = subprocess.check_output("wmic path win32_videocontroller get PNPDeviceID", shell=True, text=True)
            
            # Dividi l'output in righe
            lines = output.strip().split('\n')

            vendor_ids = []
            for line in lines[1:]:  # Ignora l'intestazione
                if "VEN_" in line:
                    # Trova il Vendor ID
                    start_index = line.find("VEN_") + 4
                    vendor_id = line[start_index:start_index+4]
                    vendor_ids.append(vendor_id)

            return vendor_ids
        
        except subprocess.CalledProcessError as e:
            print(f"Errore durante l'esecuzione del comando WMIC: {e}")
            return []

    @classmethod
    def get_gpu_manufacturer(cls):
        vendor_mapping = {
            "1002": "AMD",
            "10DE": "NVIDIA",
            "8086": "Intel"
        }

        vendor_ids = cls.get_gpu_info()
        if not vendor_ids:
            return None
        
        # Cerca il primo vendor ID corrispondente in vendor_mapping
        for vendor_id in vendor_ids:
            if vendor_id in vendor_mapping:
                return vendor_mapping[vendor_id]

        return None

    @classmethod
    def execute_ddu_command(cls, gpu_manufacturer):
        commands = {
            'AMD': f'"{cls.ddu_path}\\Display Driver Uninstaller.exe" -silent -PreventWinUpdate  -cleanamd -NoRestorePoint  -RemoveAMDCP -RemoveAMDKMPFD -RemoveAudioBus  -removeamddirs -removecrimsoncache -removemonitors -cleanallgpus',
            'NVIDIA': f'"{cls.ddu_path}\\Display Driver Uninstaller.exe" -silent -PreventWinUpdate  -cleannvidia -NoRestorePoint -RemovePhysx -RemoveGFE -RemoveNVBROADCAST -RemoveNVCP    -RemoveVulkan -removemonitors -removenvidiadirs -remove3dtvplay -cleanallgpus',
            'Intel': f'"{cls.ddu_path}\\Display Driver Uninstaller.exe" -silent -PreventWinUpdate  -cleanintel -NoRestorePoint  -RemoveINTELCP  -RemoveVulkan -removemonitors  -cleanallgpus'
        }
        command = commands.get(gpu_manufacturer)
        if command:
            try:
                subprocess.run(command, shell=True)
            except Exception as e:
                print(f"Error executing DDU command: {e}")
        else:
            print("Unsupported GPU manufacturer or no GPU detected.")

    @classmethod
    def restart_system(cls):
        try:
            subprocess.run(["shutdown", "/r", "/t", "3"], check=True)
            print("System will restart in 3 seconds.")
        except subprocess.CalledProcessError as e:
            print(f"Error initiating system restart: {e}")

    @classmethod
    def auto_uninstall(cls):
        if not cls.is_ddu_installed():
            print("DDU is not installed. Installing...")
            cls.install_ddu()
        
        cls.ddu_path = cls.find_ddu_path()
        if not cls.ddu_path:
            print("DDU installation path not found.")
            sys.exit(1)

        gpu_manufacturer = cls.get_gpu_manufacturer()
        if gpu_manufacturer:
            print(f"Detected GPU Manufacturer: {gpu_manufacturer}")
            cls.execute_ddu_command(gpu_manufacturer)
            print('il pc si riavvierà in automatico non spegnere!')
            cls.restart_system()
        else:
            print("No supported GPU manufacturer detected or an error occurred. Try to reinstall Driver.")

