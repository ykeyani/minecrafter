# minecrafter
automagically deploy minecraft spigot server to a centos 8 host (other operating systems may require minor tweaking)

## quickstart

1. on ubuntu/debian  
  `sudo apt install python3-venv`
2. install ansible to a local ./venv if you want to use the provided shortcut scripts.  
  `./setup.sh`  
  alternatively use your local installation of ansible and use the commands listed below. Also create plugins and backups directories  
  `mkdir -p ./plugins ./backups`
3. copy the inventory template:  
`cp inventory.example.yml inventory.yml`  
open it up and change:  
    - `0.0.0.0` to your servers public IP address
    - `ansible_user: root` to whatever user you will ssh into your server with.
    - `level_seed: 7257160633286220967` to whatever level seed you want or remove the line for a random seed.
    - `java_memory: 3500M` to something a little under your servers memory (M = megabytes)
    - `motd: "knowledge is power, guard it well."` to whatever dumb line you want to appear on server lists.
    - `spigot_target_version: 1.16.4` to whichever spigot minecraft build you wish to use.
    - `admin_username:` & `admin_uuid:` to whatever the admins minecraft username and uuid is.
    - `rcon_password:` to a long random string perhaps 64 characters. (note: I would recommend keeping rcon ports closed to the internet unless you plan to use it for actual remote commands.)
    - `whitelist:` to the people you want to play with adding their names/uuid and keeping the syntax and format the same as the provided examples making sure you keep the correct indentation.
4.  Choose what you want to do on your server.
    - fresh install overwriting configs  
    `./install.sh` or  
    `ansible -i inventory.yml playbook.yml --tags "install"`
    - update preserving configs  
    `./update.sh` or  
    `ansible -i inventory.yml playbook.yml --tags "update"`  
    - install mods/plugins only  
    `./plugins.sh` or  
    `ansible -i inventory.yml playbook.yml --tags "plugins"`  
    - update configs only  
    `./config.sh` or  
    `ansible -i inventory.yml playbook.yml --tags "config"`  
    - backup world, plugins and whitelist/ops  
    `./backup.sh` or  
    `ansible -i inventory.yml playbook.yml --tags "backup"`  
    - restore and install from the latest backup  
    `./restore.sh` or  
    `ansible -i inventory.yml playbook.yml --tags "restore"`  
    
## notes
- backups will be stored in ./backups
- plugin .jar(s) should be saved to ./plugins
- feel free to fork and mangle/demangle this project as much as you want.