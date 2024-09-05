import subprocess

def crea_file_batch(nome_file, contenuto):
    # Crea un file batch con il nome e il contenuto forniti
    with open(nome_file, "w") as file:
        file.write(contenuto)

def crea_requirements():
    # Elenco delle librerie da includere nel file requirements.txt
    librerie = [
        "deep-translator",
        "auto-py-to-exe",
        "pyperclip",
        "googletrans",
        "pyautogui",
        "wmi",
        "mss",
        "numpy",
        "pywin32",
        "pyyaml",
        "requests",
        "ipython",
        "psutil",
        "gitpython",
        "opencv-python==4.6.0.66",
        "scipy",
        "thop",
        "tqdm",
        "tensorboard",
        "keyboard",
        "pandas",
        "translate",
        "pytube",
        "openai",
        "rich",
        "pygame",
        "pyserial",
        "colorama",
        "pytube",
        "onnxruntime-directml",
        "pefile",
        "matplotlib",
        "seaborn",
        "gradio",
        "ultralytics"
    ]

    # Creazione del file requirements.txt
    with open("requirements.txt", "w") as file:
        for libreria in librerie:
            file.write(libreria + "\n")

def install_all():
    try:
        # Genera il file requirements.txt
        crea_requirements()

        # Contenuto del file batch per l'installazione
        contenuto_installazione = """@echo off
echo Installing Python libraries from requirements.txt...
pip install -r requirements.txt
echo Installation completed.
"""
        # Crea il file batch per l'installazione
        crea_file_batch("installa_lib.bat", contenuto_installazione)
        
        # Esegui il file batch di installazione
        subprocess.run(["installa_lib.bat"], check=True)
        print("Installazione completata con successo.")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'installazione: {e}")

def uninstall_all():
    try:
        # Contenuto del file batch per la disinstallazione
        contenuto_disinstallazione = """@echo off
echo Aggiornamento di pip alla versione più recente...
python -m pip install --upgrade pip
echo Aggiornamento di pip completato.

setlocal enabledelayedexpansion

rem Set the file path for backup
set "backup_file=backup.txt"

rem Get the list of installed Python libraries and write only the library names to backup.txt
(for /f "delims== tokens=1,*" %%A in ('pip freeze') do (
    set "library_name=%%A"
    echo !library_name!>> %backup_file%
))

echo Lista delle librerie Python installate salvata in %backup_file%.

rem Uninstall Python libraries specified in backup.txt
echo Disinstallazione delle librerie Python da backup.txt...
pip uninstall -r backup.txt -y
echo Disinstallazione completata.

rem Clean the pip cache directory
echo Pulizia della cartella cache di pip...
rmdir /s /q "%LOCALAPPDATA%\\pip\\Cache"
echo Pulizia della cartella cache completata.
"""
        # Crea il file batch per la disinstallazione
        crea_file_batch("uninstall_lib.bat", contenuto_disinstallazione)
        
        # Esegui il file batch di disinstallazione
        subprocess.run(["uninstall_lib.bat"], check=True)
        print("Disinstallazione completata con successo.")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante la disinstallazione: {e}")


