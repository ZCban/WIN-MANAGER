import winreg
import ctypes
import os
import subprocess


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_command_as_admin(command):
    if is_admin():
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            print(f"Output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr}")
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "python", f'"{os.path.abspath(__file__)}" {command}', None, 1)

def set_registry_value_current_user(path, name, value, reg_type=winreg.REG_SZ):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, name, 0, reg_type, value)
        winreg.CloseKey(key)
        print(f"La chiave '{name}' è stata impostata a {value}.")
    except Exception as e:
        print(f"Errore durante la modifica del registro: {e}")

def set_registry_value_local_machine(path, name, value, reg_type=winreg.REG_SZ):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, name, 0, reg_type, value)
        winreg.CloseKey(key)
        print(f"La chiave '{name}' è stata impostata a {value}.")
    except Exception as e:
        print(f"Errore durante la modifica del registro: {e}")

def set_Tcpip():
    set_registry_value_local_machine(r"SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters", "IRPStackSize", 32, winreg.REG_DWORD)
    set_registry_value_local_machine(r"SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters", "SizReqBuf", 17424, winreg.REG_DWORD)  # 17 kilobyte
    set_registry_value_local_machine(r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "DefaultTTL", 64, winreg.REG_DWORD)
    set_registry_value_local_machine(r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "Tcp1323Opts", 1, winreg.REG_DWORD)
    set_registry_value_local_machine(r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "MaxFreeTcbs", 65536, winreg.REG_DWORD)
    set_registry_value_local_machine(r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "MaxUserPort", 65534, winreg.REG_DWORD)
    set_registry_value_local_machine(r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "GlobalMaxTcpWindowSize", 65535, winreg.REG_DWORD)
    set_registry_value_local_machine(r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "TcpNoDelay", 1, winreg.REG_DWORD)
    set_registry_value_local_machine(r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "TcpAckFrequency", 1, winreg.REG_DWORD)

def enable_windows_defender():
    commands = [
        'reg add "HKLM\\SYSTEM\\ControlSet001\\Services\\MsSecFlt" /v "Start" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SYSTEM\\ControlSet001\\Services\\SecurityHealthService" /v "Start" /t REG_DWORD /d "3" /f',
        'reg add "HKLM\\SYSTEM\\ControlSet001\\Services\\Sense" /v "Start" /t REG_DWORD /d "3" /f',
        'reg add "HKLM\\SYSTEM\\ControlSet001\\Services\\WdBoot" /v "Start" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SYSTEM\\ControlSet001\\Services\\WdFilter" /v "Start" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SYSTEM\\ControlSet001\\Services\\WdNisDrv" /v "Start" /t REG_DWORD /d "3" /f',
        'reg add "HKLM\\SYSTEM\\ControlSet001\\Services\\WdNisSvc" /v "Start" /t REG_DWORD /d "3" /f',
        'reg add "HKLM\\SYSTEM\\ControlSet001\\Services\\WinDefend" /v "Start" /t REG_DWORD /d "2" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v "SecurityHealth" /t REG_EXPAND_SZ /d "%systemroot%\\system32\\SecurityHealthSystray.exe" /f',
        'reg add "HKLM\\SYSTEM\\ControlSet001\\Services\\SgrmAgent" /v "Start" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SYSTEM\\ControlSet001\\Services\\SgrmBroker" /v "Start" /t REG_DWORD /d "2" /f',
        'reg add "HKLM\\SYSTEM\\ControlSet001\\Services\\webthreatdefsvc" /v "Start" /t REG_DWORD /d "3" /f',
        'reg add "HKLM\\SYSTEM\\ControlSet001\\Services\\webthreatdefusersvc" /v "Start" /t REG_DWORD /d "2" /f',
        'reg delete "HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\smartscreen.exe" /f',
        'reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Associations" /f',
        'reg delete "HKLM\\Software\\Policies\\Microsoft\\Windows Defender\\SmartScreen" /f',
        'reg delete "HKLM\\Software\\Policies\\Microsoft\\Windows Defender\\Signature Updates" /f'
    ]
    for command in commands:
        run_command_as_admin(command)
    print("Windows Defender has been enabled successfully! Please restart your PC.")



def disable_firewall():
    commands = [
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\SharedAccess\\Parameters\\FirewallPolicy\\StandardProfile" /v "EnableFirewall" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\SharedAccess\\Parameters\\FirewallPolicy\\DomainProfile" /v "EnableFirewall" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\SharedAccess\\Parameters\\FirewallPolicy\\PublicProfile" /v "EnableFirewall" /t REG_DWORD /d "0" /f'
    ]
    for command in commands:
        run_command_as_admin(command)
    print("Windows Firewall has been disabled successfully!")

def disable_notifications():
    commands = [
        'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings" /v "NOC_GLOBAL_SETTING_ALLOW_TOASTS_ABOVE_LOCK" /t REG_DWORD /d "0" /f',
        'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings" /v "NOC_GLOBAL_SETTING_ALLOW_CRITICAL_TOASTS_ABOVE_LOCK" /t REG_DWORD /d "0" /f',
        'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings" /v "NOC_GLOBAL_SETTING_TOASTS_ENABLED" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Explorer" /v "DisableNotificationCenter" /t REG_DWORD /d "1" /f',
        'reg add "HKCU\\SOFTWARE\\Policies\\Microsoft\\Windows\\Explorer" /v "DisableNotificationCenter" /t REG_DWORD /d "1" /f',
        'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\PushNotifications" /v "ToastEnabled" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\PushNotifications" /v "ToastEnabled" /t REG_DWORD /d "0" /f',
        'reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\CurrentVersion\\PushNotifications" /v "NoToastApplicationNotification" /t REG_DWORD /d "1" /f',
        'reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\CurrentVersion\\PushNotifications" /v "NoTileApplicationNotification" /t REG_DWORD /d "1" /f',
        'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Explorer" /v "IsNotificationsEnabled" /t REG_DWORD /d "0" /f',
        #'taskkill /im explorer.exe /f',
        #'start explorer.exe'
    ]
    for command in commands:
        run_command_as_admin(command)
    print("Notifications have been disabled successfully.")

def disable_onedrive():
    commands = [
        'taskkill /f /im OneDrive.exe',
        'REG ADD "HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows\\OneDrive" /v "DisableFileSyncNGSC" /t REG_DWORD /d 1 /f',
        'REG ADD "HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows\\OneDrive" /v "DisableFileSync" /t REG_DWORD /d 1 /f',
        'REG ADD "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "ShowSyncProviderNotifications" /t REG_DWORD /d 0 /f'
    ]
    for command in commands:
        run_command_as_admin(command)
    print("OneDrive è stato disabilitato con successo.")



def disable_ad_tracking():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo', 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, 'Enabled', 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
        print("Pubblicità personalizzata disattivata.")
    except Exception as e:
        print(f"Errore durante la disattivazione della pubblicità personalizzata: {e}")


def disable_location_tracking():
    try:
        subprocess.run(['powershell', '-Command', 'Set-Service -Name lfsvc -StartupType Disabled'], check=True)
        subprocess.run(['powershell', '-Command', 'Stop-Service -Name lfsvc'], check=True)
        print("Tracciamento della posizione disattivato.")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante la disattivazione del tracciamento della posizione: {e}")


def disable_virtual_memory():
    try:
        # Disable automatic paging file management for all drives
        run_command_as_admin('wmic computersystem set AutomaticManagedPagefile=False')
        print("La gestione automatica del file di paging è stata disabilitata con successo.")
    except subprocess.CalledProcessError as e:
        print("Si è verificato un errore durante la disabilitazione della gestione automatica del file di paging:", e)
        print("Fallito.")

def hide_windows_updates():
    run_command_as_admin('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v "SettingsPageVisibility" /t REG_SZ /d "hide:cortana;privacy-automaticfiledownloads;privacy-feedback;windowsinsider;windowsupdate" /f')
    run_command_as_admin('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v "IsWUHidden" /t REG_DWORD /d "1" /f')
    run_command_as_admin('taskkill /im explorer.exe /f')
    run_command_as_admin('start explorer.exe')
    print("Windows Updates is now hidden!")
