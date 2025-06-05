# bin/remote_inst/userinput.py

def ask(prompt, default=None):
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    val = input(prompt)
    return val.strip() or default

def get_ssh_credentials():
    ip = ask("Remote Server IP")
    username = ask("Remote Username", "root")
    from getpass import getpass
    password = getpass("Remote Password: ")
    return ip, username, password
