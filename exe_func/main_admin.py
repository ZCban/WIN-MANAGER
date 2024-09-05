import os
import subprocess
import ctypes
import threading

# Funzione per verificare se l'account corrente è un amministratore
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Funzione per eseguire un comando con privilegi di amministratore
def run_command_as_admin(command):
    print(f"Esecuzione del comando: {command}")
    subprocess.run(f'powershell.exe -Command "{command}"', shell=True)

# Funzione per eseguire uno script come amministratore utilizzando un file .bat
def run_as_admin():
    # Ottieni il percorso dello script Python attualmente in esecuzione
    script_path = os.path.abspath(__file__)

    # Crea un file batch temporaneo
    bat_path = os.path.join(os.getenv("TEMP"), "run_as_admin.bat")
    with open(bat_path, 'w') as bat_file:
        bat_file.write(f'@echo off\n')
        bat_file.write(f'python "{script_path}"\n')  # Comando per eseguire lo script Python corrente
        bat_file.write('exit\n')

    # Usa ctypes per eseguire il file batch con privilegi di amministratore
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f'/c "{bat_path}"', None, 1)
    except Exception as e:
        print(f"Errore nell'esecuzione come amministratore: {e}")

# Abilitare UAC
def enable_uac():
    print("Abilitazione del Controllo dell'Account Utente (UAC)...")
    commands = [
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableVirtualization" /t REG_DWORD /d "1" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableInstallerDetection" /t REG_DWORD /d "1" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "PromptOnSecureDesktop" /t REG_DWORD /d "1" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableLUA" /t REG_DWORD /d "1" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableSecureUIAPaths" /t REG_DWORD /d "1" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "ConsentPromptBehaviorAdmin" /t REG_DWORD /d "5" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "ValidateAdminCodeSignatures" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableUIADesktopToggle" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "ConsentPromptBehaviorUser" /t REG_DWORD /d "3" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "FilterAdministratorToken" /t REG_DWORD /d "0" /f'
    ]
    for command in commands:
        run_command_as_admin(command)
    print("UAC abilitato con successo.")

# Disabilitare UAC
def disable_uac():
    print("Disabilitazione del Controllo dell'Account Utente (UAC)...")
    commands = [
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableVirtualization" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableInstallerDetection" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "PromptOnSecureDesktop" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableLUA" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableSecureUIAPaths" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "ConsentPromptBehaviorAdmin" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "ValidateAdminCodeSignatures" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableUIADesktopToggle" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "ConsentPromptBehaviorUser" /t REG_DWORD /d "0" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "FilterAdministratorToken" /t REG_DWORD /d "0" /f'
    ]
    for command in commands:
        run_command_as_admin(command)
    print("UAC disabilitato con successo.")

# Abilitare l'account Administrator integrato
def enable_administrator_account():
    print("Abilitazione dell'account Administrator integrato tramite PowerShell...")
    run_command_as_admin("Get-LocalUser -Name 'Administrator' | Enable-LocalUser")
    print("Account Administrator abilitato.")

# Abilitare l'account Administrator usando il Prompt dei Comandi
def enable_administrator_account_cmd():
    print("Abilitazione dell'account Administrator tramite net user...")
    run_command_as_admin("net user Administrator /active:yes")
    print("Account Administrator abilitato tramite net user.")

# Rimuovere la password dell'account Administrator
def remove_administrator_password():
    print("Rimozione della password per l'account Administrator...")
    run_command_as_admin('net user Administrator ""')
    print("Password dell'account Administrator rimossa.")


# Aggiungere l'utente corrente al gruppo Administrators
def add_user_to_administrators():
    current_user = os.getlogin()
    print(f"Verifica se il tuo account ({current_user}) è un amministratore...")
    if is_admin():
        print(f"Il tuo account ({current_user}) è un amministratore.")
    else:
        print(f"Il tuo account ({current_user}) NON è un amministratore. Aggiungendo l'utente al gruppo Administrators...")
        run_command_as_admin(f'net localgroup Administrators "{current_user}" /add')
        print(f"{current_user} è stato aggiunto al gruppo Administrators.")

# Aggiungere l'utente corrente al gruppo Administrators
def remove_user_to_administrators():
    current_user = os.getlogin()
    print(f"Verifica se il tuo account ({current_user}) è un amministratore...")
    if is_admin():
        print(f"Il tuo account ({current_user}) è un amministratore.")
        run_command_as_admin(f'net localgroup Administrators "{current_user}" /remove')
    else:
        print(f"Il tuo account ({current_user}) NON è un amministratore.")

# Funzione per riavviare il computer
def restart_computer():
    print("Riavvio del sistema in 5 secondi...")
    run_command_as_admin("shutdown /r /t 5")


def take_admin():
    if not is_admin():
        print("Esecuzione come amministratore richiesta. Riavviando lo script...")
        run_as_admin()  # Esegui lo script come amministratore
    else:
        print("Esecuzione con privilegi di amministratore.")
        # Aggiungi qui le operazioni da eseguire come amministratore
        disable_uac()
        enable_administrator_account()
        enable_administrator_account_cmd()
        remove_administrator_password()
        add_user_to_administrators()
        restart_computer()


def leave_admin():
    if is_admin():
        print("Esecuzione con privilegi di amministratore.")
        enable_uac()
        enable_administrator_account()
        enable_administrator_account_cmd()
        remove_administrator_password()
        remove_user_to_administrators()
        restart_computer()
    else:
        ('Lutente non è amministratore non serve rimuovere')
    
