#!/usr/bin/bash

mkdir build

echo "Setting Up NBIS"
sudo rm -rf ./nbis #Remove any old copies
git clone https://github.com/lbussy/nbis ./nbis
cd nbis
./setup.sh ${PWD}/../build
echo "Configuring NBIS"
make config
echo "Making NBIS"
make it
echo "Installing NBIS"
sudo make install LIBNBIS=no

echo "Checking NBIS binaries paths"
case :$PATH:
  in *:$HOME/OpenEFT/nbis/nfseg/bin:*) ;; # do nothing, it's there
     *) echo 'export PATH="$HOME/OpenEFT/nbis/nfseg/bin:$PATH"' >> ~/.bashrc #it's missing, add to PATH
esac

case :$PATH:
  in *:$HOME/OpenEFT/nbis/nfiq/bin:*) ;; # do nothing, it's there
     *) echo 'export PATH="$HOME/OpenEFT/nbis/nfiq/bin:$PATH"' >> ~/.bashrc #it's missing, add to PATH
esac

#source ~/.bashrc doesn't work in .sh in Ubuntu since scripts run in their own session. Need to run post build

echo "Installing LibOpenJP2-Tools"
sudo apt-get install libopenjp2-tools -y
sudo apt-get install libgl1-mesa-glx -y

echo "Installing Pip Requirements"

cd ~/OpenEFT
pip3 install -r requirements.txt
python3 manage.py migrate

echo "OpenEFT build complete. Update your PATH by typing 'source ~/.bashrc' and run the app by typing 'python3 openeft.py'"
cd ~/OpenEFT
source ~/.bashrc
