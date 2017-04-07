[![Build Status](https://travis-ci.org/danbev/node-rpm.svg?branch=master)](https://travis-ci.org/danbev/node-rpm)

### Node.js RPM Packaging
This project purpose is to create RPMs targeted for Fedora and RHEL.


### Releases 
Built releases are published on [github](https://github.com/danbev/node-rpm/releases).

### Building a new RPM
If there is a new version released for Node.js there is no existing staging branch for that version
a branch should be created.

The normal work flow would then be:
1. Branch off v&lt;n&gt;x-staging (where n is the major version of Node.js) 
2. Update Node.js version in [nodejs.spec](./src/nodejs.spec)
3. Either run the [build locally](#running-the-build-locally) or
  commit the changes and create a pull request against the branch in question

Both of these options will run through the build process and report back any failures. It might be
easier to run the build locally to identify the failure if there are any.

### Running the build locally

#### Build the docker image

    $ docker build -t bucharestgold/fedora-node . 

#### Run the docker image

    $ docker run -it -v ${PWD}/rpms:/root/rpmbuild/RPMS bucharestgold/fedora-node

#### Run the build manually

    $ docker run -it -v ${PWD}/rpms:/root/rpmbuild/RPMS bucharestgold/fedora-node bash

Then run the following command to build the RPM:

    $ ./run.sh

### Built RPMs
The build RPMS can be found in the [rpms](./rpms) directory and are also published when a tag
is pushed.

### Delete old containers

    $ docker rm $(docker ps -a -q)

### Increase memory limit
When runnnig the build you may require more than the default 2GB or memory.
This can be done by increasing the memory limit in Docker for Mac preferences.
If you see an error similar to this you may need to increase your memory settings:

    collect2: fatal error: ld terminated with signal 9 [Killed]
