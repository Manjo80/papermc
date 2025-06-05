# bin/remote_inst/rinstall.py

from sshclient import SSHClientWrapper
from remotesetup import remote_system_setup
from userinput import get_ssh_credentials, ask
from logger import write_info_file

def main():
    # SSH-Daten abfragen
    ip, user, pw = get_ssh_credentials()

    # Verbindung aufbauen
    ssh = SSHClientWrapper(ip, user, pw)
    try:
        ssh.connect()
        print("SSH-Verbindung aufgebaut.")

        # System und Repo vorbereiten
        remote_system_setup(ssh)

        # Beispiel für Info-Datei, später dynamisch erweitern:
        server_name = ask("Servername", "meinserver")
        data = {
            "Remote_IP": ip,
            "Remote_User": user,
            "Remote_Password": pw,
            "Servername": server_name
        }
        write_info_file(server_name, data)

    finally:
        ssh.close()
        print("Verbindung geschlossen.")

if __name__ == "__main__":
    main()
