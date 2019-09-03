#!/bin/bash
set -ev
cd $BLUEBIRD_HOME
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt -y install docker-ce
echo '{ "experimental": true }' | sudo tee /etc/docker/daemon.json
sudo service docker restart
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
# Although there is a warning, the creds are hashed on the travis end first
cat /home/travis/.docker/config.json
# If CI on master branch then tag with latest
if [ $TRAVIS_BRANCH = "master" ]; then
    docker build --tag=bluebird .
    docker tag bluebird turinginst/bluebird:latest
    docker push turinginst/bluebird:latest
fi
# If CI on release branch branch then tag with that release number
if [[ $TRAVIS_BRANCH == release* ]]; then
    echo $TRAVIS_BRANCH
    RELEASE_VERSION=`echo $TRAVIS_BRANCH | awk -F/ '{print $NF}'`
    echo $RELEASE_VERSION
    docker build --tag=bluebird .
    docker tag bluebird turinginst/bluebird:$RELEASE_VERSION
    docker push turinginst/bluebird:$RELEASE_VERSION
fi
