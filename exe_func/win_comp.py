import subprocess

def auto_install():
    # Contenuto del file batch
    batch_content = """@echo off
chcp 1252 >nul
:: Richiede l'esecuzione come amministratore
echo Sblocco completo dell'esecuzione degli script PowerShell...

:: Sbloccare completamente l'esecuzione degli script PowerShell
powershell -command "Set-ExecutionPolicy Unrestricted -Scope LocalMachine -Force"
echo Esecuzione degli script PowerShell sbloccata senza restrizioni.


@echo off
REM Controlla se Chocolatey è già installato
powershell -Command "Get-Command choco -ErrorAction SilentlyContinue" >nul 2>&1

IF %ERRORLEVEL% EQU 0 (
    echo Chocolatey è già installato.
) ELSE (
    echo Installazione di Chocolatey...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"

    IF %ERRORLEVEL% EQU 0 (
        echo Chocolatey installato con successo.
    ) ELSE (
        echo Errore nell'installazione di Chocolatey.
    )
)

@echo off
echo Inizio installazione di WinGet...

:: URLs dei file da scaricare
set "winget_url=https://aka.ms/getwinget"
set "vclibs_url=https://aka.ms/Microsoft.VCLibs.x64.14.00.Desktop.appx"
set "xaml_url=https://github.com/microsoft/microsoft-ui-xaml/releases/download/v2.7.3/Microsoft.UI.Xaml.2.7.x64.appx"

:: Nomi dei file
set "winget_file=Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle"
set "vclibs_file=Microsoft.VCLibs.x64.14.00.Desktop.appx"
set "xaml_file=Microsoft.UI.Xaml.2.7.x64.appx"

:: Scarica i file
powershell -Command "Start-BitsTransfer -Source '%winget_url%' -Destination '%winget_file%'"
echo Scaricato %winget_file%

powershell -Command "Start-BitsTransfer -Source '%vclibs_url%' -Destination '%vclibs_file%'"
echo Scaricato %vclibs_file%

powershell -Command "Start-BitsTransfer -Source '%xaml_url%' -Destination '%xaml_file%'"
echo Scaricato %xaml_file%

:: Controlla se una versione più recente di Microsoft.VCLibs è già installata
powershell -Command "Get-AppxPackage -Name Microsoft.VCLibs.140.00.UWPDesktop | Out-Null"
if %errorlevel%==0 (
    echo Microsoft.VCLibs.x64.14.00.Desktop è già installato. Skip installazione.
) else (
    powershell -Command "Add-AppxPackage %vclibs_file%"
    echo Installato %vclibs_file%
)

:: Installa gli altri pacchetti
powershell -Command "Add-AppxPackage %xaml_file%"
echo Installato %xaml_file%

powershell -Command "Add-AppxPackage %winget_file%"
echo Installato %winget_file%

:: Rimuove i file scaricati
powershell -Command "Remove-Item %winget_file%"
echo Rimosso %winget_file%

powershell -Command "Remove-Item %vclibs_file%"
echo Rimosso %vclibs_file%

powershell -Command "Remove-Item %xaml_file%"
echo Rimosso %xaml_file%

:: Verifica se %UserProfile%\AppData\Local\Microsoft\WindowsApps è nel PATH
echo Verifica del PATH...

set "windows_apps_path=%UserProfile%\AppData\Local\Microsoft\WindowsApps"
set "path_found=false"

for %%P in ("%PATH:;=" "%") do (
    if /I "%%~P"=="%windows_apps_path%" (
        set "path_found=true"
    )
)

if "%path_found%"=="false" (
    echo %windows_apps_path% non presente nel PATH. Aggiunta in corso...
    setx PATH "%PATH%;%windows_apps_path%"
    echo Percorso aggiunto al PATH.
) else (
    echo %windows_apps_path% è già presente nel PATH.
)

:: Controlla se WinGet è installato
powershell -Command "Get-Command winget | Out-Null"
if %errorlevel%==0 (
    :: Aggiorna le sorgenti di winget
    powershell -Command "winget source update"
    echo Aggiornate le sorgenti di winget
) else (
    echo WinGet non è stato installato correttamente o non è nel PATH.
)

echo Installazione completata!

@echo off

:: Installazione di tutte le librerie Visual C++ Redistributable
echo Installazione di tutte le versioni delle librerie Visual C++ Redistributable...
winget install Microsoft.VCRedist.2015+.x86 -e --accept-source-agreements
winget install Microsoft.VCRedist.2015+.x64 -e --accept-source-agreements
winget install Microsoft.VCRedist.2013.x86 -e --accept-source-agreements
winget install Microsoft.VCRedist.2013.x64 -e --accept-source-agreements
winget install Microsoft.VCRedist.2012.x86 -e --accept-source-agreements
winget install Microsoft.VCRedist.2012.x64 -e --accept-source-agreements
winget install Microsoft.VCRedist.2010.x86 -e --accept-source-agreements
winget install Microsoft.VCRedist.2010.x64 -e --accept-source-agreements
winget install Microsoft.VCRedist.2008.x86 -e --accept-source-agreements
winget install Microsoft.VCRedist.2008.x64 -e --accept-source-agreements
winget install Microsoft.VCRedist.2005.x86 -e --accept-source-agreements
winget install Microsoft.VCRedist.2005.x64 -e --accept-source-agreements

:: Installazione di DirectX
echo Installazione di DirectX...
winget install Microsoft.DirectX -e --accept-source-agreements

:: Installazione di .NET Framework
echo Installazione del .NET Framework 4.5.1...
winget install Microsoft.DotNet.Framework.DeveloperPack_4 -e --accept-source-agreements

:: Operazione completata
echo Installazione completata!
    """
    
    # Nome del file batch
    batch_file = "script.bat"
    
    # Creazione del file batch
    with open(batch_file, "w") as file:
        file.write(batch_content)
    
    # Esecuzione del file batch come amministratore
    subprocess.run(["powershell", "-Command", "Start-Process", batch_file, "-Verb", "RunAs"])


def auto_uninstall():
    # Contenuto del file batch
    batch_content = """@echo off
REM Controlla se Chocolatey è installato
powershell -Command "Get-Command choco -ErrorAction SilentlyContinue" >nul 2>&1

IF %ERRORLEVEL% EQU 0 (
    echo Disinstallazione di Chocolatey...

    REM Disinstalla Chocolatey
    powershell -NoProfile -ExecutionPolicy Bypass -Command "choco uninstall chocolatey -y" >nul 2>&1

    REM Verifica se la disinstallazione ha avuto successo
    IF %ERRORLEVEL% EQU 0 (
        echo Chocolatey disinstallato con successo.
        
        REM Pulizia dei file residui
        echo Rimozione dei file residui...
        
        REM Rimuove la cartella Chocolatey da ProgramData
        rmdir /S /Q "%ProgramData%\\chocolatey"

        REM Rimuove le variabili d'ambiente associate a Chocolatey
        SETX PATH "%PATH:C:\\ProgramData\\chocolatey\\bin;%="

        echo Pulizia completata.
    ) ELSE (
        echo Errore nella disinstallazione di Chocolatey.
    )
) ELSE (
    echo Chocolatey non è installato.
)

@echo off

REM Controlla se winget è installato
powershell -Command "Get-Command winget -ErrorAction SilentlyContinue" >nul 2>&1

IF %ERRORLEVEL% NEQ 0 (
    echo Winget non è installato. Installalo prima di eseguire questo script.
    pause
    exit /b 1
)

:: Disinstallazione di tutte le librerie Visual C++ Redistributable
echo Disinstallazione di tutte le versioni delle librerie Visual C++ Redistributable...
winget uninstall Microsoft.VCRedist.2015+.x86 -e --accept-source-agreements
winget uninstall Microsoft.VCRedist.2015+.x64 -e --accept-source-agreements
winget uninstall Microsoft.VCRedist.2013.x86 -e --accept-source-agreements
winget uninstall Microsoft.VCRedist.2013.x64 -e --accept-source-agreements
winget uninstall Microsoft.VCRedist.2012.x86 -e --accept-source-agreements
winget uninstall Microsoft.VCRedist.2012.x64 -e --accept-source-agreements
winget uninstall Microsoft.VCRedist.2010.x86 -e --accept-source-agreements
winget uninstall Microsoft.VCRedist.2010.x64 -e --accept-source-agreements
winget uninstall Microsoft.VCRedist.2008.x86 -e --accept-source-agreements
winget uninstall Microsoft.VCRedist.2008.x64 -e --accept-source-agreements
winget uninstall Microsoft.VCRedist.2005.x86 -e --accept-source-agreements
winget uninstall Microsoft.VCRedist.2005.x64 -e --accept-source-agreements

:: Disinstallazione di DirectX
echo Disinstallazione di DirectX...
winget uninstall Microsoft.DirectX -e --accept-source-agreements

:: Disinstallazione di .NET Framework
echo Disinstallazione del .NET Framework 4.5.1...
winget uninstall Microsoft.DotNet.Framework.DeveloperPack_4 -e --accept-source-agreements

:: Operazione completata
echo Disinstallazione completata!
"""
    
    # Nome del file batch
    batch_file = "disinstalla_script.bat"
    
    # Creazione del file batch
    with open(batch_file, "w") as file:
        file.write(batch_content)
    
    # Esecuzione del file batch come amministratore
    subprocess.run(["powershell", "-Command", "Start-Process", batch_file, "-Verb", "RunAs"])


