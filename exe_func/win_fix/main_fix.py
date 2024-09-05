import os
import ctypes
import sys
import time

def is_admin():
    try:
        # Verifica se l'utente ha privilegi di amministratore
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def fix():
    if not is_admin():
        print("Questo script richiede i privilegi di amministratore per essere eseguito.")
        time.sleep(10)
        sys.exit()

    from utility.energy_confg import configure_power_plan
    from utility.fixer import esegui_ripristino
    from utility.reg_restore import ripristina_registro
    from utility.install_winupdate import auto_up
    from utility.winupdate_hide import unhide_windows_updates

    configure_power_plan()
    #ripristina_registro()
    esegui_ripristino()
    #auto_up()

fix()
