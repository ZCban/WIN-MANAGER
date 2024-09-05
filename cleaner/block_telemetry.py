def block_telemetry_domains():
    try:
        with open(r'C:\Windows\System32\drivers\etc\hosts', 'a') as hosts_file:
            domains = [
                # Windows
                "127.0.0.1 vortex.data.microsoft.com",
                "127.0.0.1 vortex-win.data.microsoft.com",
                "127.0.0.1 telecommand.telemetry.microsoft.com",
                "127.0.0.1 telecommand.telemetry.microsoft.com.nsatc.net",
                "127.0.0.1 oca.telemetry.microsoft.com",
                "127.0.0.1 oca.telemetry.microsoft.com.nsatc.net",
                "127.0.0.1 sqm.telemetry.microsoft.com",
                "127.0.0.1 sqm.telemetry.microsoft.com.nsatc.net",
                "127.0.0.1 a-0001.a-msedge.net",
                "127.0.0.1 a-0002.a-msedge.net",
                "127.0.0.1 a-0003.a-msedge.net",
                "127.0.0.1 a-0004.a-msedge.net",
                "127.0.0.1 a-0005.a-msedge.net",
                "127.0.0.1 a-0006.a-msedge.net",
                "127.0.0.1 a-0007.a-msedge.net",
                "127.0.0.1 a-0008.a-msedge.net",
                "127.0.0.1 a-0009.a-msedge.net",
                "127.0.0.1 a-msedge.net",
                "127.0.0.1 asimov-win.settings.data.microsoft.com",
                "127.0.0.1 content.windows.microsoft.com",
                "127.0.0.1 df.telemetry.microsoft.com",
                "127.0.0.1 diagnostic.data.microsoft.com",
                "127.0.0.1 dl.delivery.mp.microsoft.com",
                "127.0.0.1 geo.settings.data.microsoft.com",
                "127.0.0.1 i1.services.social.microsoft.com",
                "127.0.0.1 i1.services.social.microsoft.com.nsatc.net",
                "127.0.0.1 ipv6.msftconnecttest.com",
                "127.0.0.1 msedge.net",
                "127.0.0.1 msnbot-65-55-108-23.search.msn.com",
                "127.0.0.1 msntest.serving-sys.com",
                "127.0.0.1 oca.telemetry.microsoft.com",
                "127.0.0.1 oca.telemetry.microsoft.com.nsatc.net",
                "127.0.0.1 pre.footprintpredict.com",
                "127.0.0.1 redir.metaservices.microsoft.com",
                "127.0.0.1 reports.wes.df.telemetry.microsoft.com",
                "127.0.0.1 services.wes.df.telemetry.microsoft.com",
                "127.0.0.1 settings-sandbox.data.microsoft.com",
                "127.0.0.1 settings-win.data.microsoft.com",
                "127.0.0.1 sqm.df.telemetry.microsoft.com",
                "127.0.0.1 sqm.telemetry.microsoft.com",
                "127.0.0.1 ssw.live.com",
                "127.0.0.1 statsfe1.ws.microsoft.com",
                "127.0.0.1 survey.watson.microsoft.com",
                "127.0.0.1 telecommand.telemetry.microsoft.com",
                "127.0.0.1 telecommand.telemetry.microsoft.com.nsatc.net",
                "127.0.0.1 telemetry.appex.bing.net",
                "127.0.0.1 telemetry.microsoft.com",
                "127.0.0.1 telemetry.urs.microsoft.com",
                "127.0.0.1 vortex-sandbox.data.microsoft.com",
                "127.0.0.1 vortex-win.data.microsoft.com",
                "127.0.0.1 watson.live.com",
                "127.0.0.1 watson.microsoft.com",
                "127.0.0.1 watson.ppe.telemetry.microsoft.com",
                "127.0.0.1 wes.df.telemetry.microsoft.com",
                "127.0.0.1 willcroftg.services.ms",
                "127.0.0.1 www.msftncsi.com",
            ]
            
            for domain in domains:
                hosts_file.write(f"{domain}\n")
            
            print("Domains successfully added to the hosts file.")
    except Exception as e:
        print(f"An error occurred: {e}")


import os

def remove_telemetry_domains():
    try:
        hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
        
        # Leggi il file hosts
        with open(hosts_path, 'r') as hosts_file:
            lines = hosts_file.readlines()
        
        # Lista dei domini di telemetria da rimuovere
        domains_to_remove = [
            "127.0.0.1 vortex.data.microsoft.com",
            "127.0.0.1 vortex-win.data.microsoft.com",
            "127.0.0.1 telecommand.telemetry.microsoft.com",
            "127.0.0.1 telecommand.telemetry.microsoft.com.nsatc.net",
            "127.0.0.1 oca.telemetry.microsoft.com",
            "127.0.0.1 oca.telemetry.microsoft.com.nsatc.net",
            "127.0.0.1 sqm.telemetry.microsoft.com",
            "127.0.0.1 sqm.telemetry.microsoft.com.nsatc.net",
            "127.0.0.1 a-0001.a-msedge.net",
            "127.0.0.1 a-0002.a-msedge.net",
            "127.0.0.1 a-0003.a-msedge.net",
            "127.0.0.1 a-0004.a-msedge.net",
            "127.0.0.1 a-0005.a-msedge.net",
            "127.0.0.1 a-0006.a-msedge.net",
            "127.0.0.1 a-0007.a-msedge.net",
            "127.0.0.1 a-0008.a-msedge.net",
            "127.0.0.1 a-0009.a-msedge.net",
            "127.0.0.1 a-msedge.net",
            "127.0.0.1 asimov-win.settings.data.microsoft.com",
            "127.0.0.1 content.windows.microsoft.com",
            "127.0.0.1 df.telemetry.microsoft.com",
            "127.0.0.1 diagnostic.data.microsoft.com",
            "127.0.0.1 dl.delivery.mp.microsoft.com",
            "127.0.0.1 geo.settings.data.microsoft.com",
            "127.0.0.1 i1.services.social.microsoft.com",
            "127.0.0.1 i1.services.social.microsoft.com.nsatc.net",
            "127.0.0.1 ipv6.msftconnecttest.com",
            "127.0.0.1 msedge.net",
            "127.0.0.1 msnbot-65-55-108-23.search.msn.com",
            "127.0.0.1 msntest.serving-sys.com",
            "127.0.0.1 oca.telemetry.microsoft.com",
            "127.0.0.1 oca.telemetry.microsoft.com.nsatc.net",
            "127.0.0.1 pre.footprintpredict.com",
            "127.0.0.1 redir.metaservices.microsoft.com",
            "127.0.0.1 reports.wes.df.telemetry.microsoft.com",
            "127.0.0.1 services.wes.df.telemetry.microsoft.com",
            "127.0.0.1 settings-sandbox.data.microsoft.com",
            "127.0.0.1 settings-win.data.microsoft.com",
            "127.0.0.1 sqm.df.telemetry.microsoft.com",
            "127.0.0.1 sqm.telemetry.microsoft.com",
            "127.0.0.1 ssw.live.com",
            "127.0.0.1 statsfe1.ws.microsoft.com",
            "127.0.0.1 survey.watson.microsoft.com",
            "127.0.0.1 telecommand.telemetry.microsoft.com",
            "127.0.0.1 telecommand.telemetry.microsoft.com.nsatc.net",
            "127.0.0.1 telemetry.appex.bing.net",
            "127.0.0.1 telemetry.microsoft.com",
            "127.0.0.1 telemetry.urs.microsoft.com",
            "127.0.0.1 vortex-sandbox.data.microsoft.com",
            "127.0.0.1 vortex-win.data.microsoft.com",
            "127.0.0.1 watson.live.com",
            "127.0.0.1 watson.microsoft.com",
            "127.0.0.1 watson.ppe.telemetry.microsoft.com",
            "127.0.0.1 wes.df.telemetry.microsoft.com",
            "127.0.0.1 willcroftg.services.ms",
            "127.0.0.1 www.msftncsi.com",
        ]
        
        # Filtra le linee che non contengono i domini di telemetria
        new_lines = [line for line in lines if not any(domain in line for domain in domains_to_remove)]
        
        # Scrivi il file hosts aggiornato
        with open(hosts_path, 'w') as hosts_file:
            hosts_file.writelines(new_lines)
        
        print("Le regole di telemetria sono state rimosse con successo dal file hosts.")
    
    except Exception as e:
        print(f"Si è verificato un errore durante la rimozione delle regole di telemetria: {e}")

# Esegui la funzione per rimuovere le regole di telemetria
remove_telemetry_domains()




# Esegui la funzione per bloccare i domini di telemetria
#block_telemetry_domains()
