import subprocess

def remove_systemd_service(server_type, name):
    service_name = f"{server_type}-{name}.service"
    print(f"➡️  Entferne systemd Service: {service_name}")
    subprocess.run(["systemctl", "stop", service_name])
    subprocess.run(["systemctl", "disable", service_name])
    subprocess.run(["rm", f"/etc/systemd/system/{service_name}"])
    subprocess.run(["systemctl", "daemon-reload"])
