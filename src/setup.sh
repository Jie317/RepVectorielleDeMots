#! /bin/bash
# Setup for the whole project
set -e 

if [ "$(id -u)" != "0" ]; then
   echo "Please run as root" 1>&2
   exit 1
fi

#python-dev 
sudo apt-get install python-pip python-numpy python-scipy python-matplotlib software-properties-common zlib1g-dev
sudo pip install -U scikit-learn	
sudo pip install --upgrade gensim
add-apt-repository ppa:george-edison55/cmake-3.x
sudo apt-get install cmake
sudo pip install -U nltk
export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.10.0rc0-cp27-none-linux_x86_64.whl
sudo pip install --upgrade $TF_BINARY_URL
