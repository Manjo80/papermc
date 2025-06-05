# bin/remote_inst/remotesetup.py

def remote_system_setup(ssh):
    cmds = [
        "apt update && apt install -y python3 python3-pip python3-venv openjdk-21-jre-headless curl jq unzip git",
        "mkdir -p /opt/papermc",
        "mkdir -p /opt/minecraft",
        "cd /opt/papermc && if [ -d .git ]; then git pull --rebase; else git clone https://github.com/Manjo80/papermc.git .; fi",
        "cd /opt/papermc && python3 -m venv .venv",
        "cd /opt/papermc && source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"
    ]
    for cmd in cmds:
        ssh.run(cmd)
