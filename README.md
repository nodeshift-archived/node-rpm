[![Build Status](https://travis-ci.org/danbev/node-rpm.svg?branch=master)](https://travis-ci.org/danbev/node-rpm)

### RHEL Node.js RPM Packaging image
This project exist to help me understand how Node.js is packaged as an RPM by Fedora/RHEL.

### Increase memory limit
When runnnig the build you may require more than the default 2GB or memory.
This can be done by increasing the memory limit in Docker for Mac preferences.
If you see an error similar to this you may need to increase your memory settings:

    collect2: fatal error: ld terminated with signal 9 [Killed]

### Building the Docker image

    $ docker build -t bucharestgold/fedora-node . 

### Running a Docker container

    $ docker run -it -v ${PWD}/rpms:/root/rpmbuild/RPMS bucharestgold/fedora-node

### Building the Node RPM manually

    $ docker run -it -v ${PWD}/rpms:/root/rpmbuild/RPMS bucharestgold/fedora-node bash

The run the following command to build the RPM:

    $ ./run.sh

### Built RPMs
The build RPMS can be found in the [rpms](./rpms) directory.

### Delete old containers

    $ docker rm $(docker ps -a -q)

### Updating Node.js version
When a new release as been released a branch should be create off the staging branch for the
major version in question. After this has been done the Node version should be updated in
[src/nodejs.spec](./src/nodejs.spec) and the create a pull request to have the RPMs built
with that version.

