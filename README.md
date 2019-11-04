# DEPRECATED

This is no longer supported.

[![Build Status](https://travis-ci.org/nodeshift/node-rpm.svg?branch=master)](https://travis-ci.org/nodeshift/node-rpm)

This purpose of this project is to create RPMs targeted CentOS to allow us to help identify issues
early and contribute changes upstream when possible.

The RPM [spec file](./src/nodejs.spec) was based on the spec file from this
[koji build](https://koji.fedoraproject.org/koji/buildinfo?buildID=861930).

### Releases 
Built releases are [published][] on github

### Building a new RPM
If there is a new version released for Node.js and there is no existing staging branch for that version
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

    $ docker build -t nodeshift/centos-node .

#### Run the docker image

    $ docker run -it -v ${PWD}/rpms:/root/rpmbuild/RPMS nodeshift/centos-node

#### Run the build manually

    $ docker run -it -v ${PWD}/rpms:/root/rpmbuild/RPMS nodeshift/centos-node bash

Then run the following command to build the RPM:

    $ ./run.sh

### Built RPMs
The build RPMS can be found in the [rpms](./rpms) directory and are also [published][] when a tag is pushed.

### Delete old containers

    $ docker rm $(docker ps -a -q)

### Increase memory limit
When runnnig the build you may require more than the default 2GB or memory.
This can be done by increasing the memory limit in Docker for Mac preferences.
If you see an error similar to this you may need to increase your memory settings:

    collect2: fatal error: ld terminated with signal 9 [Killed]

### RPM package information
Information about the installed RPM can be retreived using the following rpm command:
```console
[root@e8b41340469a node-rpm]# rpm -qi rhoar-nodejs 
Name        : rhoar-nodejs
Epoch       : 1
Version     : 8.8.0
Release     : 1.el7
Architecture: x86_64
Install Date: Thu Oct 26 07:07:30 2017
Group       : Development/Languages
Size        : 26254177
License     : MIT and ASL 2.0 and ISC and BSD
Signature   : (none)
Source RPM  : rhoar-nodejs-8.8.0-1.el7.src.rpm
Build Date  : Wed Oct 25 13:25:39 2017
Build Host  : e8b41340469a
Relocations : (not relocatable)
URL         : http://nodejs.org/
Summary     : JavaScript runtime
Description :
Node.js is a platform built on Chrome's JavaScript runtime
for easily building fast, scalable network applications.
Node.js uses an event-driven, non-blocking I/O model that
makes it lightweight and efficient, perfect for data-intensive
real-time applications that run across distributed devices.
```
### License information
License information can be retrieved using the following rpm command:

    $ rpm -qa rhoar-nodejs --qf "%{name}: %{license}\n"
    rhoar-nodejs: MIT and ASL 2.0 and ISC and BSD

    $ rpm -q -L rhoar-nodejs
    /usr/share/licenses/rhoar-nodejs-8.9.1/LICENSE
    /usr/share/licenses/rhoar-nodejs-8.9.1/license.html
    /usr/share/licenses/rhoar-nodejs-8.9.1/license.xml
    /usr/share/licenses/rhoar-nodejs-8.9.1/licenses.css

### Useful RPM commands
To find the package that a node executable belongs to:

    $ which node
    $ rpm -qf /usr/bin/node
    rhoar-nodejs-8.8.0-1.el7.x86_64

To list the documentation for an install rpm:

    $ rpm -qd rhoar-nodejs
    /usr/share/doc/rhoar-nodejs-8.8.0/AUTHORS
    /usr/share/doc/rhoar-nodejs-8.8.0/CHANGELOG.md
    /usr/share/doc/rhoar-nodejs-8.8.0/COLLABORATOR_GUIDE.md
    /usr/share/doc/rhoar-nodejs-8.8.0/GOVERNANCE.md
    /usr/share/doc/rhoar-nodejs-8.8.0/README.md
    /usr/share/doc/rhoar-nodejs-8.8.0/license.xml
    /usr/share/doc/rhoar-nodejs-8.8.0/license.html
    /usr/share/doc/rhoar-nodejs-8.8.0/licenses.css
    ...

[published]: https://github.com/nodeshift/node-rpm/releases

