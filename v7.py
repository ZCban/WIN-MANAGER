import tkinter as tk
from tkinter import ttk, scrolledtext
from exe_func.win_comp import auto_install, auto_uninstall
from exe_func.app_management import start_user_uninstallation, start_user_installation, user_update_all_apps, apps
from exe_func.sys_cleaner import clean_windows
from exe_func.main_admin import take_admin
from exe_func.attiva_windows import attiva
from exe_func.defender_delete import Remove_defender
from exe_func.driver_manager.DDU_CleanGrafics import DisplayDriverUninstaller
from exe_func.driver_manager.Device_Manager import DriverInstaller
from exe_func.python_manager.python_manager import uninstall_all, install_all
from exe_func import win_fix
from exe_func.regedit_tweaks import (
    set_Tcpip,
    disable_firewall,
    disable_notifications,
    disable_onedrive,
    disable_ad_tracking,
    disable_location_tracking
)
from exe_func.PnP_Remover import clean_non_connected_devices

# Function to insert text into the terminal and scroll to the end
def terminal_insert(text):
    terminal.insert(tk.END, text)
    terminal.see(tk.END)

# Function to clear the terminal
def clear_terminal():
    terminal.delete(1.0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Installatore di Applicazioni con Winget")

# Create the main frame
frame_main = ttk.Frame(root)
frame_main.pack(padx=10, pady=10, fill="both", expand=True)

# Create a Notebook for different sections
notebook = ttk.Notebook(frame_main)
notebook.pack(padx=10, pady=10, fill="both", expand=True)

# Frame for Main Functionalities
frame_main_funcs = ttk.Frame(notebook)
notebook.add(frame_main_funcs, text="Main Functionalities")

# Grid configuration for Main Functionalities buttons
frame_main_funcs.grid_columnconfigure(0, weight=1)
frame_main_funcs.grid_columnconfigure(1, weight=1)
frame_main_funcs.grid_columnconfigure(2, weight=1)
frame_main_funcs.grid_columnconfigure(3, weight=1)

# Creazione del bottone "Take Admin"
btn_take_admin = ttk.Button(frame_main_funcs, text="Take Admin", command=lambda: take_admin())
btn_take_admin.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

# Creazione del bottone "Install Win Comp"
btn_install_win_comp = ttk.Button(frame_main_funcs, text="Install Win Comp", command=lambda: auto_install())
btn_install_win_comp.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Creazione del bottone "Uninstall Win Comp"
btn_uninstall_win_comp = ttk.Button(frame_main_funcs, text="Uninstall Win Comp", command=lambda: auto_uninstall())
btn_uninstall_win_comp.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

# Creazione del bottone "Clean Windows"
btn_clean_windows = ttk.Button(frame_main_funcs, text="Clean Windows", command=lambda: clean_windows(terminal_insert))
btn_clean_windows.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

# Creazione del bottone "Activate Windows"
btn_activate_windows = ttk.Button(frame_main_funcs, text="Activate Windows", command=lambda: attiva(terminal_insert))
btn_activate_windows.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

# Creazione del bottone "DDU Auto Clean"
btn_auto_uninstall = ttk.Button(frame_main_funcs, text="DDU Auto Clean", command=lambda: DisplayDriverUninstaller.auto_uninstall())
btn_auto_uninstall.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Creazione del bottone "Auto Install Drivers"
btn_auto_install_drivers = ttk.Button(frame_main_funcs, text="Auto Install Drivers", command=lambda: DriverInstaller.auto_install_drivers())
btn_auto_install_drivers.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

# Creazione del bottone "Remove Non-Connected Devices"
btn_remove_non_connected_devices = ttk.Button(frame_main_funcs, text="Remove Non-Connected Devices", command=lambda: clean_non_connected_devices())
btn_remove_non_connected_devices.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

# Scrolled text terminal to show the installation progress
terminal = scrolledtext.ScrolledText(frame_main_funcs, height=15, bg="black", fg="green", font=("Consolas", 10))
terminal.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")


# Frame for App Management
frame_apps = ttk.Frame(notebook)
notebook.add(frame_apps, text="App Management")

sorted_apps = sorted(apps, key=lambda app: app[0].lower())
app_vars = {}
rows_per_column = (len(sorted_apps) + 2) // 3

for index, (app_name, app_id) in enumerate(sorted_apps):
    var = tk.BooleanVar()
    chk = ttk.Checkbutton(frame_apps, text=app_name, variable=var)
    column = index // rows_per_column
    row = index % rows_per_column
    chk.grid(row=row, column=column, sticky="w", padx=5, pady=5)
    app_vars[app_id] = var

btn_start_install = ttk.Button(frame_apps, text="Install", command=lambda: start_user_installation(app_vars, terminal_insert))
btn_start_install.grid(row=rows_per_column, column=0, pady=5)
btn_start_uninstall = ttk.Button(frame_apps, text="Uninstall", command=lambda: start_user_uninstallation(app_vars, terminal_insert))
btn_start_uninstall.grid(row=rows_per_column, column=1, pady=5)
btn_update_apps = ttk.Button(frame_apps, text="Update All Apps", command=lambda: user_update_all_apps(terminal_insert))
btn_update_apps.grid(row=rows_per_column, column=2, pady=5)

# Frame for Python Manager
frame_python_manager = ttk.Frame(notebook)
notebook.add(frame_python_manager, text="Python Manager")

btn_uninstall_all = ttk.Button(frame_python_manager, text="Uninstall All", command=lambda: uninstall_all())
btn_uninstall_all.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

btn_install_all = ttk.Button(frame_python_manager, text="Install All", command=lambda: install_all())
btn_install_all.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Frame for Regedit Tweaks
frame_regedit_tweaks = ttk.Frame(notebook)
notebook.add(frame_regedit_tweaks, text="Regedit Tweaks")

btn_improve_ping = ttk.Button(frame_regedit_tweaks, text="set_Tcpip", command=lambda: set_Tcpip())
btn_improve_ping.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

btn_disable_defender = ttk.Button(frame_regedit_tweaks, text="Disable Windows Defender", command=lambda: Remove_defender())
btn_disable_defender.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

btn_disable_firewall = ttk.Button(frame_regedit_tweaks, text="Disable Firewall", command=lambda: disable_firewall())
btn_disable_firewall.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

btn_disable_notifications = ttk.Button(frame_regedit_tweaks, text="Disable Notifications", command=lambda: disable_notifications())
btn_disable_notifications.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

btn_disable_onedrive = ttk.Button(frame_regedit_tweaks, text="Disable OneDrive", command=lambda: disable_onedrive())
btn_disable_onedrive.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

btn_disable_ad_tracking = ttk.Button(frame_regedit_tweaks, text="Disable Ad Tracking", command=lambda: disable_ad_tracking())
btn_disable_ad_tracking.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

btn_disable_location_tracking = ttk.Button(frame_regedit_tweaks, text="Disable Location Tracking", command=lambda: disable_location_tracking())
btn_disable_location_tracking.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

# Frame for Terminal and Other Controls
frame_terminal_controls = ttk.Frame(frame_main)
frame_terminal_controls.pack(side="bottom", fill="x")

btn_clear_terminal = ttk.Button(frame_terminal_controls, text="Clear Terminal", command=clear_terminal)
btn_clear_terminal.pack(side="left", padx=5, pady=5)

btn_exit = ttk.Button(frame_terminal_controls, text="Exit", command=root.quit)
btn_exit.pack(side="right", padx=5, pady=5)

# Start the main window loop
root.mainloop()
