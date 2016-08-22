#!/bin/bash
# Setup for the whole project

if [ "$(id -u)" != "0" ]; then
   echo "Please run as root" 1>&2
   exit 1
fi

if [ $? -eq 0 ]; then
	apt-get install python-pip python-dev python-numpy python-scipy python-matplotlib software-properties-common zlib1g-dev
	if [ $? -eq 0 ]; then
		pip install -U scikit-learn	
		if [ $? -eq 0 ]; then
			pip install --upgrade gensim
			if [ $? -eq 0 ]; then
				add-apt-repository ppa:george-edison55/cmake-3.x
				apt-get install cmake
				if [ $? -eq 0 ]; then
					pip install -U nltk
					if [ $? -eq 0 ]; then
						export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.10.0rc0-cp27-none-linux_x86_64.whl
						pip install --upgrade $TF_BINARY_URL
					fi
				fi
			fi
		fi
	fi	
fi














