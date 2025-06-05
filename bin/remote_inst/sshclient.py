# bin/remote_inst/sshclient.py

import paramiko

class SSHClientWrapper:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.ip, username=self.username, password=self.password)

    def run(self, command):
        print(f"SSH> {command}")
        stdin, stdout, stderr = self.client.exec_command(command)
        out = stdout.read().decode()
        err = stderr.read().decode()
        if out:
            print(out)
        if err:
            print("FEHLER:", err)
        return out, err

    def sftp_put(self, local_path, remote_path):
        with self.client.open_sftp() as sftp:
            print(f"SFTP> {local_path} -> {remote_path}")
            sftp.put(local_path, remote_path)

    def close(self):
        if self.client:
            self.client.close()
