# Minecraft Server Manager

A modular Bash-based management system for deploying and managing PaperMC and Velocity Minecraft servers on Linux.  
Supports automated setup, centralized RCON control, and proxy configuration through Velocity.

## Features
- Create and configure standalone or Velocity-integrated PaperMC servers
- Install and configure Velocity proxy
- Enable and manage RCON access for all servers
- Centralized RCON control across multiple servers
- Clean, modular script structure
- No manual editing of config files required

## Requirements
- Linux with `bash` and `systemd`
- Packages:
  - `git`
  - `curl`
  - `jq`
  - `unzip`
  - `yq`
  - `openjdk-21-jre-headless`
  - `mcrcon`

## Usage

```bash
apt install git -y
git clone https://github.com/manjo80/papermc.git
cd papermc
chmod +x manager.sh
./manager.sh
