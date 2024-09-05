import subprocess
import winreg
import threading

# Elenco delle chiavi di prodotto
keys = [
    "46V6N-VCBYR-KT9KT-6Y4YF-QGJYH",  # Windows 8
    "V7C3N-3W6CM-PDKR2-KW8DQ-RJMRD",  # Windows 8 Professional
    "7QNT4-HJDDR-T672J-FBFP4-2J8X9",  # Windows 8 N
    "4NX4X-C98R3-KBR22-MGBWC-D667X",  # Windows 8 Professional N
    "NH7GX-2BPDT-FDPBD-WD893-RJMQ4",  # Windows 8 Single Language
    "NTTX3-RV7VB-T7X7F-WQYYY-9Y92",   # Windows 8.1 Preview
    "46J3N-RY6B3-BJFDY-VBFT9-V22HG",  # Windows 10 Home
    "PGGM7-N77TC-KVR98-D82KJ-DGPHV",  # Windows 10 Home N
    "RHGJR-N7FVY-Q3B8F-KBQ6V-46YP4",  # Windows 10 Pro
    "GH37Y-TNG7X-PP2TK-CMRMT-D3WV4",  # Windows 10 SL
    "68WP7-N2JMW-B676K-WR24Q-9D7YC",  # Windows 10 CHN SL
    "37GNV-YCQVD-38XP9-T848R-FC2HD",  # Windows 10 Home
    "33CY4-NPKCC-V98JP-42G8W-VH636",  # Windows 10 Home N
    "NF6HC-QH89W-F8WYV-WWXV4-WFG6P",  # Windows 10 Pro
    "NH7W7-BMC3R-4W9XT-94B6D-TCQG3",  # Windows 10 Pro N
    "NTRHT-XTHTG-GBWCG-4MTMP-HH64C",  # Windows 10 SL
    "7B6NC-V3438-TRQG7-8TCCX-H6DDY",  # Windows 10 CHN SL
    "YTMG3-N6DKC-DKB77-7M9GH-8HVX7",  # Windows 10 Home
    "4CPRK-NM3K3-X6XXQ-RXX86-WXCHW",  # Windows 10 Home N
    "BT79Q-G7N6G-PGBYW-4YWX6-6F4BT",  # Windows 10 Home Single Language
    "VK7JG-NPHTM-C97JM-9MPGT-3V66T",  # Windows 10 Pro
    "2B87N-8KFHP-DKV6R-Y2C8J-PKCKT",  # Windows 10 Pro N
    "DXG7C-N36C4-C4HTG-X4T3X-2YV77",  # Windows 10 Pro for Workstations
    "WYPNQ-8C467-V2W6J-TX4WX-WT2RQ",  # Windows 10 Pro N for Workstations
    "3NF4D-GF9GY-63VKH-QRC3V-7QW8P",  # Windows 10 S
    "YNMGQ-8RYV3-4PGQ3-C8XTP-7CFBY",  # Windows 10 Education
    "84NGF-MHBT6-FXBX8-QWJK7-DRR8H",  # Windows 10 Education N
    "8PTT6-RNW4C-6V7J2-C2D3X-MHBPB",  # Windows 10 Pro Education
    "GJTYN-HDMQY-FRR76-HVGC7-QPF8P",  # Windows 10 Pro Education N
    "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",  # Windows 11 Home
    "3KHY7-WNT83-DGQKR-F7HPR-844BM",  # Windows 11 Home N
    "7HNRX-D7KGG-3K4RQ-4WPJ4-YTDFH",  # Windows 11 Home Single Language
    "PVMJN-6DFY6-9CCP6-7BKTT-D3WVR",  # Windows 11 Home Country Specific
    "W269N-WFGWX-YVC9B-4J6C9-T83GX",  # Windows 11 Pro
    "MH37W-N47XK-V7XM9-C7227-GCQG9",  # Windows 11 Pro N
    "NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J",  # Windows 11 Pro for Workstations
    "9FNHH-K3HBT-3W4TD-6383H-6XYWF",  # Windows 11 Pro for Workstations N
    "6TP4R-GNPTD-KYYHQ-7B7DP-J447Y",  # Windows 11 Pro Education
    "YVWGF-BXNMC-HTQYQ-CPQ99-66QFC",  # Windows 11 Pro Education N
    "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",  # Windows 11 Education
    "2WH4N-8QGBV-H22JP-CT43Q-MDWWJ",  # Windows 11 Education N
    "NPPR9-FWDCX-D2C8J-H872K-2YT43",  # Windows 10 Enterprise
    "DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4",  # Windows 10 Enterprise N
    "WNMTR-4C88C-JK8YV-HQ7T2-76DF9",  # Windows 10 Enterprise 2015 LTSB
    "2F77B-TNFGY-69QQF-B8YKP-D69TJ",  # Windows 10 Enterprise 2015 LTSB N
    "DCPHK-NFMTC-H88MJ-PFHPY-QJ4BJ",  # Windows 10 Enterprise 2016 LTSB
    "QFFDN-GRT3P-VKWWX-X7T3R-8B639",  # Windows 10 Enterprise 2016 LTSB N
    "MNXKQ-WY2CT-JWBJ2-T68TQ-YBH2V",  # Windows 10 Enterprise N Eval
    "7TNX7-H36JG-QFF42-K4JYV-YY482",  # Windows 10 Enterprise S Eval
    "D3M8K-4YN49-89KYG-4F3DR-TVJW3",  # Windows 10 Enterprise S N Eval
    "VPMWD-PVNRR-79WJ9-VVJQC-3YH2G",  # Windows 10 Enterprise Eval
    "D6RD9-D4N8T-RT9QX-YW6YT-FCWWJ",  # Windows 10 Starter
    "YNMGQ-8RYV3-4PGQ3-C8XTP-7CFBY",  # Windows 10 Education
    "84NGF-MHBT6-FXBX8-QWJK7-DRR8H",  # Windows 10 Education N
    "YTMG3-N6DKC-DKB77-7M9GH-8HVX7",  # Windows 10 Home
    "4CPRK-NM3K3-X6XXQ-RXX86-WXCHW",  # Windows 10 Home N
    "BT79Q-G7N6G-PGBYW-4YWX6-6F4BT",  # Windows 10 Core Single Language
    "N2434-X9D7W-8PF6X-8DV9T-8TYMD",  # Windows 10 Core Country Specific
    "XGVPP-NMH47-7TTHJ-W3FW7-8HV2C",  # Windows 10 Enterprise
    "NK96Y-D9CD8-W44CQ-R8YTK-DYJWX",  # Windows 10 Enterprise S
    "WGGHN-J84D6-QYCPR-T7PJ7-X766F",  # Windows 10 Enterprise N
    "FW7NV-4T673-HF4VX-9X4MM-B4H4T",  # Windows 10 Enterprise G N
    "RW7WN-FMT44-KRGBK-G44WK-QV7YK",  # Windows 10 Enterprise N LTSB 2016
    "DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4",  # Windows 10 Enterprise N (duplicato)
    "W269N-WFGWX-YVC9B-4J6C9-T83GX",  # Windows 11 Pro (duplicato)
    "MH37W-N47XK-V7XM9-C7227-GCQG9",  # Windows 11 Pro N (duplicato)
    "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",  # Windows 11 Home (duplicato)
    "WNMTR-4C88C-JK8YV-HQ7T2-76DF9",  # Windows 10 Enterprise 2015 LTSB (duplicato)
    "W269N-WFGWX-YVC9B-4J6C9-T83GX",   # Windows 11 Pro (duplicato)
    "NW9MP-GRTT8-3RXM9-W446T-XQBQB",
    "FF4BY-KVGJ9-9JXWT-BTYXT-9PQG6",
    "TN2BV-MPH84-RK4TY-286MC-6JCK2",
    "YYHW7-4BN8M-WMP3C-X2HFD-PYRX3",
    "82QVG-NCR88-PPMYH-F43T8-D9PRK",
    "36VRN-YBT32-WPRM6-C9YDV-M4G6Y",
    "P8CNG-8MBW9-FRHDB-YHTCH-M4G6Y",
    "NRGK8-DBW6B-RKWGY-6HJM3-GF4CF",
    "VK7JG-NPHTM-C97JM-9MPGT-3V66T",
    "PBHCJ-Q2NYD-2PX34-T2TD6-233PK",
    "6P99N-YF42M-TPGBG-9VMJP-YKHCF",
    "8N67H-M3CY9-QT7C4-2TR7M-TXYCV",
    "W269N-WFGWX-YVC9B-4J6C9-T83GX",
    "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",
    "3KHY7-WNT83-DGQKR-F7HPR-844BM",
    "7HNRX-D7KGG-3K4RQ-4WPJ4-YTDFH",
    "PVMJN-6DFY6-9CCP6-7BKTT-D3WVR",
    "W269N-WFGWX-YVC9B-4J6C9-T83GX",
    "MH37W-N47XK-V7XM9-C7227-GCQG9",
    "NPPR9-FWDCX-D2C8J-H872K-2YT43",
    "DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4",
    "YYVX9-NTFWV-6MDM3-9PT4T-4M68B",
    "44RPN-FTY23-9VTTB-MP9BX-T84FV",
    "M7XTQ-FN8P6-TTKYV-9D4CC-J462D",
    "92NFX-8DJQP-P6BBQ-THF9C-7CG2H",
    "6TP4R-GNPTD-KYYHQ-7B7DP-J447Y",
    "YVWGF-BXNMC-HTQYQ-CPQ99-66QFC",
    "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
    "2WH4N-8QGBV-H22JP-CT43Q-MDWWJ",
    "6RBBT-F8VPQ-QCPVQ-KHRB8-RMV82",  # Windows 7 Starter
    "FJGCP-4DFJD-GJY49-VJBQ7-HYRR2",  # Windows 7 Home Basic
    "YKHFT-KW986-GK4PY-FDWYH-7TP9F",  # Windows 7 Home Premium
    "2WCJK-R8B4Y-BKJGW-MGX3R-7QW8P", 
    "VQB3X-Q3KP8-WJ2H8-R6B6D-7QJB7",  
    "6P99N-YF42M-TPGBG-9VMJP-YKHCF",  # Windows 8 Core
    "8N67H-M3CY9-QT7C4-2TR7M-TXYCV",  # Windows 8 Professional
    "6PNFM-QMRPK-3GFXF-XJW84-C3T9F",  # Windows 8 Enterprise
    "W269N-WFGWX-YVC9B-4J6C9-T83GX",  # Windows 10 Pro
    "6P99N-YF42M-TPGBG-9VMJP-YKHCF",  # Windows 10 Home
    "3KHY7-WNT83-DGQKR-F7HPR-844BM",  # Windows 10 Home N
    "YTMG3-N6DKC-DKB77-7M9GH-8HVX7",  # Windows 10 Education
    "84NGF-MHBT6-FXBX8-QWJK7-DRR8H",  # Windows 10 Education N
    "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",  # Windows 10 Home Single Language
    "BT79Q-G7N6G-PGBYW-4YWX6-6F4BT",  # Windows 10 Home Country Specific
    "VK7JG-NPHTM-C97JM-9MPGT-3V66T",  # Windows 10 Pro
    "2B87N-8KFHP-DKV6R-Y2C8J-PKCKT",  # Windows 10 Pro N
    "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",  # Windows 11 Home
    "3KHY7-WNT83-DGQKR-F7HPR-844BM",  # Windows 11 Home N
    "7HNRX-D7KGG-3K4RQ-4WPJ4-YTDFH",  # Windows 11 Home Single Language
    "PVMJN-6DFY6-9CCP6-7BKTT-D3WVR",  # Windows 11 Home Country Specific
    "W269N-WFGWX-YVC9B-4J6C9-T83GX",  # Windows 11 Pro
    "MH37W-N47XK-V7XM9-C7227-GCQG9",  # Windows 11 Pro N
    "6TP4R-GNPTD-KYYHQ-7B7DP-J447Y",  # Windows 11 Pro Education
    "YVWGF-BXNMC-HTQYQ-CPQ99-66QFC",  # Windows 11 Pro Education N
    "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",  # Windows 11 Education
    "2WH4N-8QGBV-H22JP-CT43Q-MDWWJ"   # Windows 11 Education N
    
    
    
    
]

def get_current_product_key():
    try:
        registry_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform"
        key_name = "BackupProductKeyDefault"
        
        # Apri la chiave di registro
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path, 0, winreg.KEY_READ) as reg_key:
            current_key, _ = winreg.QueryValueEx(reg_key, key_name)
            return current_key
    except WindowsError as e:
        print(f"Errore durante l'accesso al registro di sistema: {e}")
        return None

def change_product_key(key):
    try:
        # Imposta la chiave di prodotto
        subprocess.run(f"cscript //B //Nologo C:\\Windows\\System32\\slmgr.vbs /ipk {key}", check=True, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Tenta di attivare
        result = subprocess.run("cscript //B //Nologo C:\\Windows\\System32\\slmgr.vbs /ato", check=True, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Chiave valida trovata e attivata: {key}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Errore con la chiave {key}: {e.stderr}")
        return False


def attiva_windows(terminal_insert):
    # Get the current product key
    current_key = get_current_product_key()
    
    # Iterate through the list of product keys
    for key in keys:
        if key != current_key:
            if change_product_key(key):
                terminal_insert(f"Activated successfully with key: {key}")
                return  # Exit the function after successful activation
    # If no key was found to activate
    terminal_insert("Nessuna chiave valida trovata.")


def attiva(terminal_insert):
    threading.Thread(target=attiva_windows, args=(terminal_insert,)).start()

