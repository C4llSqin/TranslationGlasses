#!/bin/bash

### Prerequisites
sudo apt update
sudo apt upgrade
sudo apt install git
sudo apt-get install curl
sudo apt-get install gnupg
sudo apt-get install ca-certificates
sudo apt-get install lsb-release

### Download the docker gpg file
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

### Add Docker and docker compose to the packages list
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-pluginsudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-pluginlinux/ubuntu   $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

### Make Docker Group
sudo groupadd docker
sudo usermod -aG docker $USER

### Git clone LibreTranslate
cd ~
git clone https://github.com/LibreTranslate/LibreTranslate.git
cd LibreTranslate

docker-compose up -d --build