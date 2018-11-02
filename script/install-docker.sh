#/bin/bash
# install packages to allow apt to use a repository over HTTPS:
sudo apt-get -y install \
apt-transport-https ca-certificates curl software-properties-common
# add Docker’s official GPG key:
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# set up the Docker stable repository.
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
# update the apt package index:
sudo apt-get -y update
# finally, install docker
sudo apt-get -y install docker-ce

curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
  sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update

sudo apt-get install nvidia-docker2
sudo pkill -SIGHUP dockerd
