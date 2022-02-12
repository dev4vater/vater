#!/bin/bash

buildPath="/tmp/sem-build/src/github.com/ansible-semaphore"
cd $buildPath

sourcePath="$buildPath/semaphore"

# Install go, task, and npm
sudo rm -rf /usr/local/go && tar -C /usr/local -xzf go1.17.6.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.17.6.linux-amd64.tar.gz
sudo snap install task --classic
sudo apt install npm -y

# Get the semaphore source
mkdir -p $buildPath
git clone --recursive https://github.com/ansible-semaphore/semaphore.git $sourcePath

cd $sourcePath

task -d $sourcePath deps
task -d $sourcePath compile

go run $sourcePath/cli/main.go setup
go run $sourcePath/cli/main.go service --config $sourcePath/config.json

git --git-dir $sourcePath/.git remote set-url origin https://github.com/rmfirth/semaphore.git
git --git-dir $sourcePath/.git fetch

rm -f  $sourcePath/web2/package-lock.json

git --git-dir $sourcePath/.git checkout rfirth/cherryPick
sed -i 's^db/migrations/*^db/**/migrations/*^' $sourcePath/Taskfile.yml

task -d $sourcePath compile

sudo context=prod tag=local task -d $sourcePath docker:build
sudo docker image prune -f
