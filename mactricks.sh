brew install libsodium
brew link libsodium
brew install zeromq --with-libsodium
brew link zeromq
sudo pip-3.3 uninstall pyzmq
sudo pip-3.3 install pyzmq