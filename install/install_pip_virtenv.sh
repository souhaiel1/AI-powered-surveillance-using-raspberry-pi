wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo python3 get-pip.py
sudo rm -rf ~/.cache/pip
sudo pip install virtualenv virtualenvwrapper

echo "
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
" >> $HOME/.bashrc

source ~/.bashrc
