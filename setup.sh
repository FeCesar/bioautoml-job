#! /bin/bash

# Get the bioautoml and install dependecy modules
cd ~

git clone https://github.com/Bonidia/BioAutoML.git BioAutoML

cd ~/BioAutoML

git pull
git submodule init
git submodule update

# Install miniconda
cd ~

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

cd ~/miniconda

chmod +x Miniconda3-latest-Linux-x86_64.sh

./Miniconda3-latest-Linux-x86_64.sh

export PATH=~/miniconda3/bin:$PATH

# Create environment
conda env create -f BioAutoML-env.yml -n bioautoml

# Run the job
pip install -r ~/bioautoml-job/requirements.txt
python ~/bioautoml-job/src/main.py