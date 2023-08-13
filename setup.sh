#! /bin/bash

# Get the bioautoml and install dependecy modules
cd ~

git clone https://github.com/Bonidia/BioAutoML.git BioAutoML

cd ~/BioAutoML

git pull
git submodule init
git submodule update

# Run the job
apt-get update -y
apt-get upgrade -y
apt-get install -y python3-pip
pip install -r ~/bioautoml-job/requirements.txt

now=$(date +"%Y-%m-%d %H:%M:%S")
nohup python3 ~/bioautoml-job/src/main.py > ~/cd-outputs/output-$now.log 2>&1 &

disown
exit
