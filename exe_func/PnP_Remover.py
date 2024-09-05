import os
import subprocess
import ctypes
import json
from ctypes import wintypes
import threading

class PnpRemover:
    @staticmethod
    def get_pnp_devices_powershell():
        """Get PnP devices using PowerShell."""
        command = "powershell -Command \"Get-PnpDevice | Select-Object -Property FriendlyName, Present, InstanceId | ConvertTo-Json\""
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        devices = json.loads(result.stdout)
        return devices

    @staticmethod
    def remove_device(instance_id):
        """Remove a device using its instance ID with pnputil command."""
        result = subprocess.run(["pnputil", "/remove-device", instance_id], capture_output=True, text=True)
        return result.stdout

    @staticmethod
    def remove_non_connected_devices():
        """Remove non-connected devices."""
        # Get all devices using PowerShell
        devices = PnpRemover.get_pnp_devices_powershell()

        # Filter out non-connected devices
        non_connected_devices = [d for d in devices if not d["Present"]]

        print("\nElenco dei dispositivi Non collegati:")
        if non_connected_devices:
            for device in non_connected_devices:
                print(f"{device['FriendlyName']} - Non collegato")

            print("\nInizio rimozione dei dispositivi non collegati...")
            for device in non_connected_devices:
                print(f"Rimozione del dispositivo: {device['FriendlyName']}")
                output = PnpRemover.remove_device(device["InstanceId"])
                print(output)
            print("Rimozione completata.")
        else:
            print("Nessun dispositivo non collegato trovato.")

        # Remove old log file from desktop if it exists
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        log_file = os.path.join(desktop_path, "OldDeviceLog.txt")
        if os.path.exists(log_file):
            os.remove(log_file)

def clean_non_connected_devices():
    PnpRemover.remove_non_connected_devices()




