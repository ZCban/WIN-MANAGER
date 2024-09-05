import winreg
import ctypes
import wmi
import subprocess

def is_uac_enabled():
    try:
        reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
        reg_name = "EnableLUA"

        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
        value, reg_type = winreg.QueryValueEx(key, reg_name)
        winreg.CloseKey(key)

        return value == 1
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error checking UAC status: {e}")
        return None

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_windows_activation():
    try:
        output = subprocess.check_output(
            ["powershell", "-Command", "(Get-WmiObject -query 'select * from SoftwareLicensingProduct where PartialProductKey is not null and LicenseStatus=1').LicenseStatus"],
            text=True
        )
        return "1" in output
    except subprocess.CalledProcessError as e:
        print(f"Error checking Windows activation status: {e}")
        return None


def is_windows_defender_enabled():
    try:
        c = wmi.WMI()
        for product in c.Win32_Product(Name="Windows Defender Antivirus"):
            return True
        return False
    except Exception as e:
        print(f"Error checking Windows Defender status: {e}")
        return None


def is_firewall_enabled():
    try:
        firewall_status = subprocess.check_output(
            ["netsh", "advfirewall", "show", "allprofiles"],
            text=True
        )
        return "State ON" in firewall_status
    except Exception as e:
        print(f"Error checking Firewall status: {e}")
        return None

def get_windows_version():
    try:
        return subprocess.check_output(["ver"], shell=True, text=True).strip()
    except Exception as e:
        print(f"Error retrieving Windows version: {e}")
        return None

def is_windows_activated():
    try:
        output = subprocess.check_output(["slmgr", "/xpr"], text=True)
        return "The machine is permanently activated" in output or "The machine is activated" in output
    except Exception as e:
        print(f"Error checking Windows activation status: {e}")
        return None


def is_windows_update_enabled():
    try:
        c = wmi.WMI()
        service = c.Win32_Service(Name='wuauserv')
        if service:
            service = service[0]
            return service.StartMode == "Auto" and service.State == "Running"
        return False
    except Exception as e:
        print(f"Error checking Windows Update status: {e}")
        return None

def is_fingerprint_enabled():
    try:
        c = wmi.WMI()
        biometric_devices = c.Win32_BiometricDevice()
        for device in biometric_devices:
            if 'fingerprint' in device.Caption.lower():
                return True
        return False
    except Exception as e:
        return None

def is_winget_installed():
    try:
        subprocess.check_output(["winget", "--version"], text=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def is_choco_installed():
    try:
        subprocess.check_output(["choco", "-v"], text=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def is_python_installed():
    try:
        subprocess.check_output(["python", "--version"], text=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.check_output(["python3", "--version"], text=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

def is_backup_service_enabled():
    try:
        c = wmi.WMI()
        service = c.Win32_Service(Name='SDRSVC')
        if service:
            service = service[0]
            return service.StartMode == "Auto" and service.State == "Running"
        return False
    except Exception as e:
        return None

def is_bitlocker_enabled():
    try:
        c = wmi.WMI()
        for volume in c.Win32_EncryptableVolume():
            if volume.ProtectionStatus == 1:
                return True
        return False
    except Exception as e:
        return None

def is_system_restore_enabled():
    try:
        c = wmi.WMI()
        for sr in c.Win32_SystemRestore():
            if sr.SequenceNumber is not None:
                return True
        return False
    except Exception as e:
        return None

def is_wsl_installed():
    try:
        subprocess.check_output(["wsl", "--list"], text=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def are_automatic_updates_enabled():
    try:
        reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update"
        reg_name = "AUOptions"
        
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
        value, reg_type = winreg.QueryValueEx(key, reg_name)
        winreg.CloseKey(key)
        
        return value in [3, 4]
    except Exception as e:
        return None


def is_tpm_enabled():
    try:
        output = subprocess.check_output(
            ["powershell", "-Command", "(Get-WmiObject -Namespace \"Root\\CIMv2\\Security\\MicrosoftTpm\" -Class Win32_Tpm).IsEnabled_InitialValue"],
            text=True
        )
        return "True" in output
    except subprocess.CalledProcessError as e:
        print(f"Error checking TPM status: {e}")
        return None

def is_secure_boot_enabled():
    try:
        reg_path = r"SYSTEM\CurrentControlSet\Control\SecureBoot\State"
        reg_name = "UEFISecureBootEnabled"

        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
        value, reg_type = winreg.QueryValueEx(key, reg_name)
        winreg.CloseKey(key)

        return value == 1
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error checking Secure Boot status: {e}")
        return None



if __name__ == "__main__":
    uac_status = is_uac_enabled()
    admin_status = is_admin()
    defender_status = is_windows_defender_enabled()
    firewall_status = is_firewall_enabled()
    windows_version = get_windows_version()
    windows_activated = check_windows_activation()
    windows_update_status = is_windows_update_enabled()
    winget_status = is_winget_installed()
    choco_status = is_choco_installed()
    python_status = is_python_installed()
    backup_service_status = is_backup_service_enabled()
    bitlocker_status = is_bitlocker_enabled()
    system_restore_status = is_system_restore_enabled()
    wsl_status = is_wsl_installed()
    auto_updates_status = are_automatic_updates_enabled()
    tpm_status = is_tpm_enabled()
    secure_boot_status = is_secure_boot_enabled()

    print(f"##########################################################################")
    if uac_status is None:
        print("Unable to determine UAC status.")
    elif uac_status:
        print("UAC is enabled.")
    else:
        print("UAC is disabled.")

    if admin_status:
        print("The user has administrative privileges.")
    else:
        print("The user does not have administrative privileges.")

    if defender_status is None:
        print("Unable to determine Windows Defender status.")
    elif defender_status:
        print("Windows Defender is enabled.")
    else:
        print("Windows Defender is disabled.")

    if firewall_status is None:
        print("Unable to determine Firewall status.")
    elif firewall_status:
        print("Windows Firewall is enabled.")
    else:
        print("Windows Firewall is disabled.")

    if windows_version:
        print(f"Windows version: {windows_version}")
    else:
        print("Unable to determine Windows version.")

    if windows_activated is None:
        print("Unable to determine Windows activation status.")
    elif windows_activated:
        print("Windows is activated.")
    else:
        print("Windows is not activated.")

    if tpm_status is None:
        print("Unable to determine TPM status.")
    elif tpm_status:
        print("TPM is enabled.")
    else:
        print("TPM is not enabled.")

    if secure_boot_status is None:
        print("Unable to determine Secure Boot status.")
    elif secure_boot_status:
        print("Secure Boot is enabled.")
    else:
        print("Secure Boot is not enabled.")
        
    if windows_update_status is None:
        print("Unable to determine Windows Update status.")
    elif windows_update_status:
        print("Windows Update is enabled and running.")
    else:
        print("Windows Update is not enabled or not running.")

              

    print(f"winget installed: {'Yes' if winget_status else 'No'}")
    print(f"Chocolatey installed: {'Yes' if choco_status else 'No'}")
    print(f"Python installed: {'Yes' if python_status else 'No'}")
    print(f"Backup Service enabled: {'Yes' if backup_service_status else 'No'}")
    print(f"BitLocker enabled: {'Yes' if bitlocker_status else 'No'}")
    print(f"System Restore enabled: {'Yes' if system_restore_status else 'No'}")
    print(f"WSL installed: {'Yes' if wsl_status else 'No'}")
    print(f"Automatic Updates enabled: {'Yes' if auto_updates_status else 'No'}")
    print(f"##########################################################################")
    

