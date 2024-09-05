import subprocess
import os
import sys
import time
import platform
import wmi
import shutil

class DriverInstaller:
    wmi_instance = wmi.WMI()

    @classmethod
    def install_chocolatey(cls):
        try:
            install_command = (
                "Set-ExecutionPolicy Bypass -Scope Process -Force; "
                "[System.Net.ServicePointManager]::SecurityProtocol = "
                "[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; "
                "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
            )
            subprocess.run(["powershell", "-Command", install_command], check=True)
            print("Chocolatey installato con successo.")
        except subprocess.CalledProcessError as e:
            print(f"Errore nell'installazione di Chocolatey: {e}")





    @classmethod
    def install_intel_network_drivers_win10(cls):
        try:
            command = 'choco install intel-network-drivers-win10 -y'
            subprocess.run(command, shell=True, check=True)
            print("Intel Network Drivers for Windows 10 installation initiated.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during installation: {e}")




    @classmethod
    def restart_system(cls):
        try:
            subprocess.run(["shutdown", "/r", "/t", "6"], check=True)
            print("System will restart in 3 seconds.")
        except subprocess.CalledProcessError as e:
            print(f"Error initiating system restart: {e}")

    

    @classmethod
    def get_cpu_info(cls):
        cpu_info = {'Processor': platform.processor()}
        try:
            for cpu in cls.wmi_instance.Win32_Processor():
                cpu_info.update({
                    'Name': cpu.Name,
                    'Manufacturer': cpu.Manufacturer,
                    'NumberOfCores': cpu.NumberOfCores,
                    'NumberOfLogicalProcessors': cpu.NumberOfLogicalProcessors,
                    'PNPDeviceID': cpu.PNPDeviceID
                })
        except Exception as e:
            print(f"Error retrieving CPU info: {e}")
        return cpu_info

    @classmethod
    def get_gpu_info(cls):
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


    @classmethod
    def get_audio_info(cls):
        audio_info = []
        try:
            for sound in cls.wmi_instance.Win32_SoundDevice():
                audio_info.append({
                    'Name': sound.Name,
                    'Manufacturer': sound.Manufacturer,
                    'Status': sound.Status
                })
        except Exception as e:
            print(f"Error retrieving audio info: {e}")
        return audio_info

    @classmethod
    def get_printer_info_usb(cls):
        printer_info = []
        try:
            for device in cls.wmi_instance.Win32_PnPEntity():
                # Check for common printer-related keywords
                if device.Description and any(keyword in device.Description.lower() for keyword in ['printer', 'print']):
                    printer_info.append({
                        'Name': device.Name,
                        'Description': device.Description,
                        'PNPDeviceID': device.PNPDeviceID,
                        'Status': device.Status
                    })
        except Exception as e:
            print(f"Error retrieving printer info: {e}")
        return printer_info

    @classmethod
    def auto_install_drivers(cls):
        cls.install_chocolatey()
        cpu_info = cls.get_cpu_info()
        gpu_vendor_ids= cls.get_gpu_info()

        print(f"Checking CPU devices...")
        cpu_manufacturer = cpu_info.get('Manufacturer', '').lower()
        if 'amd' in cpu_manufacturer:
            print(f"AMD CPU detected. Installing Amd ryzen drivers.")
            subprocess.run(["choco","install", "amd-ryzen-chipset", "-y","--force"], check=True)
        elif 'intel' in cpu_manufacturer:
            print("Support for Intel CPU drivers is not yet implemented.")
        else:
            print(f"CPU manufacturer {cpu_manufacturer} not supported for automatic driver installation.")

        print(f"Checking GPU devices...")
        for vendor_id in gpu_vendor_ids:
            vendor_id = vendor_id.upper()  # Ensure vendor_id is in uppercase for comparison
            if '10DE' in vendor_id:
                print(f"NVIDIA GPU detected. Installing NVIDIA drivers.")
                subprocess.run(["choco", "install", "nvidia-display-driver", "-y",'--force'], check=True)
            elif '1002' in vendor_id:
                print('AMD GPU detected. Support for AMD GPU drivers is not yet implemented.')
            elif '8086' in vendor_id:
                print(f"Intel GPU detected. Installing Intel drivers.")
                subprocess.run(["choco", "install", "intel-arc-graphics-driver", "-y",'--force'], check=True)
            else:
                print(f"GPU with Vendor ID {vendor_id} not supported for automatic driver installation.")

        # Check and install audio drivers if Realtek is found
        print("Retrieving audio information...")
        audio_infos = cls.get_audio_info()
        for audio_info in audio_infos:
            print(f"Checking audio device: {audio_info.get('Name', '')}")
            if 'realtek' in audio_info.get('Name', '').lower():
                print("Realtek audio device found, initiating driver installation.")
                subprocess.run(["choco", "install", "realtek-hd-audio-driver", "-y",'--force'], check=True)
            else:
                print("audio device not supported.")

        # Check and install Samsung Universal Printer Driver if Samsung printer is found
        print("Retrieving printer information...")
        printer_infos = cls.get_printer_info_usb()
        for printer_info in printer_infos:
            description_lower = printer_info.get('Description', '').lower()
            print(f"Checking printer device: {printer_info.get('Description', '')}")
            if 'samsung' in description_lower:
                print("Samsung printer found, initiating driver installation.")
                subprocess.run(["choco", "install", "supd2", "-y"], check=True)
            elif 'hp' in description_lower:
                print("HP printer found, initiating driver installation.")
                subprocess.run(["choco", "install", "hp-universal-print-driver-pcl", "-y"], check=True)
            else:
                print("printer device not supported.")

        cls. restart_system()

    @classmethod
    def auto_uninstall_drivers(cls):
        cls.install_chocolatey()
        cpu_info = cls.get_cpu_info()
        gpu_vendor_ids= cls.get_gpu_info()

        cpu_manufacturer = cpu_info.get('Manufacturer', '').lower()
        if 'amd' in cpu_manufacturer:
            subprocess.run(["choco","uninstall", "amd-ryzen-chipset", "-y","--force"], check=True)
        elif 'intel' in cpu_manufacturer:
            print("Support for Intel CPU drivers is not yet implemented.")
        else:
            print(f"CPU manufacturer {cpu_manufacturer} not supported for automatic driver installation.")

        print(f"Checking GPU devices...")
        for vendor_id in gpu_vendor_ids:
            vendor_id = vendor_id.upper()  # Ensure vendor_id is in uppercase for comparison
            if '10DE' in vendor_id:
                print(f"NVIDIA GPU detected. Installing NVIDIA drivers.")
                subprocess.run(["choco", "uninstall", "nvidia-display-driver", "-y",'--force'], check=True)
            elif '1002' in vendor_id:
                print('AMD GPU detected. Support for AMD GPU drivers is not yet implemented.')
            elif '8086' in vendor_id:
                print(f"Intel GPU detected. Installing Intel drivers.")
                subprocess.run(["choco", "uninstall", "intel-arc-graphics-driver", "-y",'--force'], check=True)
            else:
                print(f"GPU with Vendor ID {vendor_id} not supported for automatic driver installation.")

        # Check and install audio drivers if Realtek is found
        print("Retrieving audio information...")
        audio_infos = cls.get_audio_info()
        for audio_info in audio_infos:
            print(f"Checking audio device: {audio_info.get('Name', '')}")
            if 'realtek' in audio_info.get('Name', '').lower():
                print("Realtek audio device found, initiating driver installation.")
                subprocess.run(["choco", "uninstall", "realtek-hd-audio-driver", "-y"], check=True)
            else:
                print("audio device not supported.")

        # Check and install Samsung Universal Printer Driver if Samsung printer is found
        print("Retrieving printer information...")
        printer_infos = cls.get_printer_info_usb()
        for printer_info in printer_infos:
            description_lower = printer_info.get('Description', '').lower()
            print(f"Checking printer device: {printer_info.get('Description', '')}")
            if 'samsung' in description_lower:
                print("Samsung printer found, initiating driver installation.")
                subprocess.run(["choco", "uninstall", "supd2", "-y"], check=True)
            elif 'hp' in description_lower:
                print("HP printer found, initiating driver installation.")
                subprocess.run(["choco", "uninstall", "hp-universal-print-driver-pcl", "-y"], check=True)
            else:
                print("printer device not supported.")

        #cls. restart_system()




