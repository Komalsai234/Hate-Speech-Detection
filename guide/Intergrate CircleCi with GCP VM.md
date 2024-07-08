# Integrating CircleCI with GCP Virtual Machine

## Integrating CircleCI with GCP VM: A Step-by-Step Guide

### Step 1: Update and Install Dependencies
 ```bash
    sudo apt update
    sudo apt-get update
    sudo apt-get upgrade -y
```

### Step 2: Install Docker
 ```bash
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker YOUR_USERNAME
    newgrp docker
```
Replace `YOUR_USERNAME` with your VM's username.

### ### Step 3: Install Google Cloud SDK
 ```bash
    curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-409.0.0-linux-x86_64.tar.gz
    tar -xf google-cloud-cli-409.0.0-linux-x86_64.tar.gz
    ./google-cloud-sdk/install.sh --path-update true
```

### Step 4: Download CircleCI Launch Agent
 ```bash
    mkdir configurations
    cd configurations
    curl https://raw.githubusercontent.com/CircleCI-Public/runner-installation-files/main/download-launch-agent.sh > download-launch-agent.sh
    sh ./download-launch-agent.sh
```

### Step 5: Create CircleCI User and Directory
 ```bash
    sudo adduser --disabled-password --gecos GECOS circleci
    sudo mkdir -p /var/opt/circleci
    sudo chmod 0750 /var/opt/circleci
    sudo chown -R circleci /var/opt/circleci
```

### Step 6: Configure CircleCI Launch Agent
 ```bash
    sudo mkdir -p /etc/opt/circleci
    sudo nano /etc/opt/circleci/launch-agent-config.yaml
```
Add the following configuration to `launch-agent-config.yaml`:
```
api:
  auth_token: YOUR_AUTH_TOKEN_HERE

runner:
  name: self-hosted
  working_directory: /var/opt/circleci/workdir
  cleanup_working_directory: true
```
### Step 7: Adjust Permissions for Configuration File
 ```bash
    sudo chown circleci: /etc/opt/circleci/launch-agent-config.yaml
    sudo chmod 600 /etc/opt/circleci/launch-agent-config.yaml
```

### Step 8: Create System Service File
 ```bash
    sudo nano /usr/lib/systemd/system/circleci.service
```
Add the following content to `circleci.service`:

```
[Unit]
Description=CircleCI Runner
After=network.target

[Service]
ExecStart=/opt/circleci/circleci-launch-agent --config /etc/opt/circleci/launch-agent-config.yaml
Restart=always
User=circleci
NotifyAccess=exec
TimeoutStopSec=18300

[Install]
WantedBy=multi-user.target
```

### Step 9: Adjust Permissions for Systemd Service File
 ```bash
    sudo chown root: /usr/lib/systemd/system/circleci.service
sudo chmod 644 /usr/lib/systemd/system/circleci.service
```


### Step 10: Enable and Start CircleCI Service
 ```bash
    sudo systemctl enable circleci.service
    sudo systemctl start circleci.service
    sudo systemctl restart circleci.service
    sudo systemctl status circleci.service
```

### Step 11: Final Setup and Verification
Restart your VM instance to ensure all changes take effect.