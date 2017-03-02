### RHEL Node.js RPM Packaging image
This project exist to help me understand how Node.js is packaged as an RPM by Fedora/RHEL.

### Cloning the git repo

    $ git clone -b rhscl-2.4-rh-nodejs6-rhel-7 git://pkgs.devel.redhat.com/rpms/nodejs rpm-repo

### Building the Docker image

    $ docker build -t danbev/fedora-node .

### Running a Docker container

    $ docker run -ti danbev/fedora-node

### Building the Node RPM
Before running rpmbuild I needed to remove the `BuildRequirement` for scldev as it could not be found.
I'm pretty sure this might be because access to the Software Collection dev might be private, but this
is something I'll look into.

    $ rpmbuild -ba nodejs.spec

