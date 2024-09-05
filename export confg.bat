@echo off
set desktop=%USERPROFILE%\Desktop
set backup_folder=%desktop%\Backup_Configurazioni

:: Crea la cartella sul desktop
mkdir "%backup_folder%"

:: Esporta Servizi di Sistema
reg export "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services" "%backup_folder%\servizi_sistema.reg"

:: Esporta Configurazioni di Group Policy
reg export "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies" "%backup_folder%\group_policy.reg"
reg export "HKEY_CURRENT_USER\Software\Policies" "%backup_folder%\user_group_policy.reg"

:: Esporta Configurazioni di Firewall dal Registro
reg export "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy" "%backup_folder%\firewall_policy.reg"

:: Esporta Configurazioni di Power Management dal Registro
reg export "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Power" "%backup_folder%\power_management.reg"
reg export "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Power\User\PowerSchemes" "%backup_folder%\power_schemes.reg"

:: Esporta Configurazioni di Rete dal Registro
reg export "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip" "%backup_folder%\tcpip_config.reg"
reg export "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Dnscache" "%backup_folder%\dns_config.reg"
reg export "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NetBT" "%backup_folder%\netbt_config.reg"

:: Esporta Configurazioni della Barra delle Applicazioni
reg export "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Taskband" "%backup_folder%\taskbar_config.reg"

:: Esporta Disposizione delle Icone del Desktop
reg export "HKEY_CURRENT_USER\Software\Microsoft\Windows\Shell\Bags" "%backup_folder%\desktop_icons_bags.reg"
reg export "HKEY_CURRENT_USER\Software\Microsoft\Windows\Shell\BagMRU" "%backup_folder%\desktop_icons_bagmru.reg"

:: Esporta Preferenze di Esplora File
reg export "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" "%backup_folder%\explorer_advanced.reg"

:: Esporta Impostazioni di Personalizzazione
reg export "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" "%backup_folder%\themes_personalize.reg"
reg export "HKEY_CURRENT_USER\Control Panel\Desktop" "%backup_folder%\control_panel_desktop.reg"

:: Esporta Impostazioni di Visualizzazione
reg export "HKEY_CURRENT_USER\Control Panel\Desktop\WindowMetrics" "%backup_folder%\display_settings.reg"

:: Esporta Configurazioni della Barra delle Lingue
reg export "HKEY_CURRENT_USER\Software\Microsoft\CTF" "%backup_folder%\language_bar.reg"
reg export "HKEY_CURRENT_USER\Keyboard Layout\Preload" "%backup_folder%\keyboard_layout.reg"

:: Esporta Impostazioni di Notifica
reg export "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\PushNotifications" "%backup_folder%\push_notifications.reg"

:: Esporta Impostazioni di Accesso Facilitato
reg export "HKEY_CURRENT_USER\Control Panel\Accessibility" "%backup_folder%\accessibility.reg"

:: Esporta Preferenze Audio
reg export "HKEY_CURRENT_USER\AppEvents\Schemes" "%backup_folder%\audio_schemes.reg"

:: Esporta Configurazioni di Microsoft Edge
reg export "HKEY_CURRENT_USER\Software\Microsoft\Edge" "%backup_folder%\edge_settings.reg"

:: Esporta Configurazioni di Internet Explorer
reg export "HKEY_CURRENT_USER\Software\Microsoft\Internet Explorer" "%backup_folder%\ie_settings.reg"

echo Operazione completata! I file .reg sono stati salvati nella cartella %backup_folder%.

@echo off
setlocal enabledelayedexpansion

set desktop=%USERPROFILE%\Desktop
set servizi_folder=%desktop%\Servizi

:: Crea la cartella Servizi sul desktop
mkdir "%servizi_folder%"

:: Percorso della chiave di registro dei servizi di sistema
set services_key=HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services

echo Esportazione dei servizi di sistema in file .reg separati...

:: Enumerazione delle sottochiavi nella chiave dei servizi
for /f "skip=2 tokens=*" %%s in ('reg query "%services_key%"') do (
    set "service_key=%%s"
    set "service_name=%%~nxs"
    echo Esportazione del servizio !service_name!...
    reg export "!service_key!" "%servizi_folder%\!service_name!.reg" /y
)

echo Esportazione completata! I file sono stati salvati nella cartella %servizi_folder%.
pause

