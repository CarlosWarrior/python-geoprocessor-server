#!/bin/bash
sudo apt-get update
sudo apt-get install curl
curl –O https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
bash Anaconda3-2020.02-Linux-x86_64.sh
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py";
python get-pip.py;
bash ./Anaconda3-2021.11-Linux-x86_64.sh;
git clone https://github.com/CarlosWarrior/python-geoprocessor-server.git;
cd python-geoprocessor-server;
sudo apt install zip
unzip -d ./storage ./storage/static.zip
conda env create --file geoprocessor-server.yml --name geoprocessor;
conda env list;
conda activate geoprocessor;

chmod +x /app.py;
python /app.py &> /output.log;  