import socket
from concurrent.futures import ThreadPoolExecutor

SERVICE_DB = {
    7: "Echo",
    19: "Chargen",
    20: "FTP-Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    26: "RSFTP",
    37: "Time",
    43: "WHOIS",
    49: "TACACS",
    53: "DNS",
    67: "DHCP-Server",
    68: "DHCP-Client",
    69: "TFTP",
    70: "Gopher",
    79: "Finger",
    80: "HTTP",
    88: "Kerberos",
    102: "ISO-TSAP",
    109: "POP2",
    110: "POP3",
    111: "RPCBind",
    113: "Ident",
    119: "NNTP",
    123: "NTP",
    135: "MSRPC",
    137: "NetBIOS-NS",
    138: "NetBIOS-DGM",
    139: "NetBIOS-SSN",
    143: "IMAP",
    161: "SNMP",
    162: "SNMP-Trap",
    177: "XDMCP",
    179: "BGP",
    194: "IRC",
    201: "AppleTalk",
    264: "BGMP",
    318: "TSP",
    381: "HP OpenView",
    382: "HP OpenView",
    383: "HP OpenView",
    389: "LDAP",
    411: "Direct Connect",
    412: "Direct Connect",
    443: "HTTPS",
    445: "SMB",
    464: "Kerberos",
    465: "SMTPS",
    497: "Dantz Retrospect",
    500: "ISAKMP",
    512: "Exec",
    513: "Login",
    514: "Shell",
    515: "Printer",
    520: "RIP",
    521: "RIPng",
    540: "UUCP",
    543: "Klogin",
    544: "Kshell",
    546: "DHCPv6-Client",
    547: "DHCPv6-Server",
    548: "AFP",
    554: "RTSP",
    563: "NNTP over SSL",
    587: "SMTP (Submission)",
    591: "FileMaker",
    593: "MSRPC over HTTPS",
    631: "IPP",
    636: "LDAPS",
    639: "MSDP",
    646: "LDP",
    691: "MS Exchange",
    860: "iSCSI",
    873: "rsync",
    902: "VMware Server",
    989: "FTPS-DATA",
    990: "FTPS",
    993: "IMAPS",
    995: "POP3S",
    1025: "Microsoft RPC",
    1026: "Windows Messenger",
    1029: "Microsoft Messenger",
    1080: "SOCKS Proxy",
    1194: "OpenVPN",
    1214: "Kazaa",
    1241: "Nessus",
    1311: "Dell OpenManage",
    1337: "Waste",
    1433: "MSSQL",
    1434: "MSSQL Monitor",
    1512: "WINS",
    1521: "Oracle DB",
    1723: "PPTP",
    1725: "Steam",
    1741: "CiscoWorks 2000",
    1755: "MS Media Server",
    1812: "RADIUS",
    1863: "MSN Messenger",
    1935: "Adobe Flash",
    1985: "Cisco HSRP",
    2000: "Cisco SCCP",
    2049: "NFS",
    2082: "cPanel",
    2083: "cPanel SSL",
    2100: "Oracle XDB",
    2222: "DirectAdmin",
    2302: "Halo",
    2483: "Oracle DB SSL",
    2484: "Oracle DB SSL",
    3000: "Node.js",
    3128: "Squid Proxy",
    3306: "MySQL",
    3389: "RDP",
    3396: "Novell NDPS",
    3689: "iTunes",
    3690: "SVN",
    3724: "World of Warcraft",
    3784: "Ventrilo",
    4333: "mSQL",
    4444: "Metasploit",
    4500: "IPSec NAT-T",
    4664: "Google Desktop",
    4672: "eMule",
    4899: "Radmin",
    5000: "UPnP",
    5001: "Synology",
    5004: "RTP",
    5005: "RTP",
    5050: "Yahoo Messenger",
    5060: "SIP",
    5190: "AIM/ICQ",
    5222: "XMPP",
    5223: "XMPP SSL",
    5432: "PostgreSQL",
    5500: "VNC",
    5631: "pcAnywhere",
    5632: "pcAnywhere",
    5800: "VNC over HTTP",
    5900: "VNC",
    5901: "VNC",
    6000: "X11",
    6001: "X11",
    6112: "Battle.net",
    6129: "DameWare",
    6257: "WinMX",
    6346: "Gnutella",
    6347: "Gnutella",
    6881: "BitTorrent",
    6969: "BitTorrent",
    7000: "Azureus",
    7001: "WebLogic",
    7002: "WebLogic SSL",
    7070: "RealServer",
    7547: "CWMP",
    8000: "HTTP Alternate",
    8008: "HTTP Alternate",
    8009: "AJP",
    8080: "HTTP Proxy",
    8081: "HTTP Proxy",
    8087: "Parallels Plesk",
    8118: "Privoxy",
    8200: "VMware Server",
    8222: "VMware Server",
    8291: "Winbox",
    8333: "Bitcoin",
    8443: "HTTPS Alternate",
    8500: "Adobe ColdFusion",
    8767: "TeamSpeak",
    8880: "HTTP Alternate",
    8888: "HTTP Alternate",
    9000: "SonarQube",
    9001: "Tor",
    9043: "WebSphere",
    9060: "WebSphere",
    9080: "WebSphere",
    9090: "WebSphere",
    9091: "Openfire Admin",
    9100: "Printer",
    9101: "Bacula",
    9102: "Bacula",
    9103: "Bacula",
    9119: "MXit",
    9150: "Tor",
    9300: "IBM Cognos",
    9418: "Git",
    9443: "VMware VSphere",
    9999: "Urchin",
    10000: "Webmin",
    10001: "Ubiquiti",
    10050: "Zabbix Agent",
    10051: "Zabbix Server",
    10161: "SNMP-Trap",
    11211: "Memcached",
    12345: "NetBus",
    13720: "NetBackup",
    13721: "NetBackup",
    14567: "Battlefield",
    15118: "Dipnet",
    19226: "AdminSecure",
    19638: "Ensim",
    20000: "Usermin",
    24800: "Synergy",
    25999: "Xfire",
    27015: "Steam",
    27017: "MongoDB",
    27018: "MongoDB",
    27374: "Sub7",
    27960: "Quake",
    31337: "Back Orifice",
    32768: "Filenet TMS",
    33434: "Traceroute",
    47808: "BACnet",
}

def scan_port(host, port):
    """
    Scan single port
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            
            if result == 0:
                service = SERVICE_DB.get(port, "Unknown Service")
                print(f"[+] Port {port} ({service}): TERBUKA")
                return port, True, service
            else:
                # Optional: tampilkan port tertutup juga
                print(f"[-] Port {port}: Tertutup")
                return port, False, None
                
    except socket.timeout:
        print(f"[!] Port {port}: Timeout")
        return port, False, None
    except ConnectionRefusedError:
        print(f"[-] Port {port}: Connection refused")
        return port, False, None
    except Exception as e:
        print(f"[!] Port {port}: Error - {e}")
        return port, False, None

def port_scanner_service_only(host):
    print(f"Memindai {host}...")
    print(f"Hanya memindai port yang memiliki layanan diketahui...")
    
    ports_to_scan = list(SERVICE_DB.keys())
    print(f"Total port yang akan discan: {len(ports_to_scan)}")
    
    open_ports = []
    
    try:
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(scan_port, host, port) 
                      for port in ports_to_scan]
            
            for future in futures:
                try:
                    # PERBAIKAN: unpack dengan benar
                    port, is_open, service = future.result(timeout=2)
                    
                    if is_open:
                        print(f"[+] Port {port} ({service}): TERBUKA")
                        open_ports.append((port, service))
                        
                except TimeoutError:
                    print(f"[!] Timeout scanning port")
                except Exception as e:
                    print(f"[!] Error processing result: {e}")
    
    except Exception as e:
        print(f"[!] Scanner error: {e}")
    
    # Tampilkan hasil
    print(f"\nScan selesai. Found {len(open_ports)} open ports.")
    return open_ports

def save_results(filename, host, open_ports, scan_type="normal"):
    """Simpan hasil scan ke file"""
    import datetime
    
    with open(filename, 'a') as f:
        f.write(f"================\n")
        f.write(f"Port Scan Report\n")
        f.write(f"================\n")
        f.write(f"Target: {host}\n")
        f.write(f"Scan Time: {datetime.datetime.now()}\n")
        f.write(f"Scan Type: {scan_type}\n")
        f.write(f"Open Ports: {len(open_ports)}\n")
        f.write(f"\n")
        f.write(f"{'PORT':<10} {'SERVICE':<30} {'STATUS':<10}\n")
        f.write(f"{'-'*50}\n")
        
        for port, service in open_ports:
            f.write(f"{port:<10} {service:<30} {'OPEN':<10}\n")
        
        # Tambahkan rekomendasi keamanan
        f.write(f"\n")
        f.write(f"RECOMMENDATIONS:\n")
        for port, service in open_ports:
            if port in [23, 21, 137, 138, 139, 445]:
                f.write(f"- Port {port} ({service}): Consider closing this port for security\n")
            elif port in [22, 3389]:
                f.write(f"- Port {port} ({service}): Ensure strong authentication is enabled\n")
    
    print(f"\n[+] Results saved to {filename}")

# Penggunaan
def main():
    print('=' * 35)
    print((' ' * 8) + 'Simple Port Scanner' + (' ' * 8))
    print('=' * 35)
    user_input = input("(1) Scan Single Port\n(2) Scan Multiple Port\n(3) Exit\nSelect Option : ")
    print('=' * 35)
    if user_input == "1":
        host = input("Masukkan host : ")
        port = int(input("Masukkan port : "))
        
        # Simpan hasil scan
        scan_result = scan_port(host, port)
        
        # Buat list dari hasil single port
        if scan_result[1]:  # Jika port terbuka
            open_ports = [(scan_result[0], scan_result[2])]  # (port, service)
        else:
            open_ports = []
            print("Port tertutup, tidak ada yang disimpan.")
        
        save = input('Ingin simpan hasil? (Y): ').upper()
        if save == 'Y':
            nama_file = input('Nama file : ')
            save_results(nama_file, host, open_ports, scan_type='normal')
        
        main()
        
    elif user_input == "2":
        host = input("Masukkan host : ")
        
        # Simpan hasil scan ke variabel
        open_ports = port_scanner_service_only(host)
        
        if open_ports:  # Jika ada port terbuka
            save = input('Ingin simpan hasil? (Y) : ').upper()
            if save == 'Y':
                nama_file = input('Nama file : ')
                save_results(nama_file, host, open_ports, scan_type='normal')
        else:
            print("Tidak ada port terbuka.")
        
        main()
        
    elif user_input == "3":
        print('Goodbye and Thank You! :)')
        SystemExit
    else:
        print("Invalid Input!")
        main()

main()