### RHEL Node.js RPM Packaging image
This project exist to help me understand how Node.js is packaged as an RPM by Fedora/RHEL.

### Cloning the git repo

    $ git clone -b rhscl-2.4-rh-nodejs6-rhel-7 git://pkgs.devel.redhat.com/rpms/nodejs rpm-repo

### Increase memory limit
When runnnig the build you may require more than the default 2GB or memory.
This can be done by increasing the memory limit in Docker for Mac preferences.
If you see an error similar to this you may need to increase your memory settings:

    collect2: fatal error: ld terminated with signal 9 [Killed]

### Building the Docker image

    $ docker build -t danbev/fedora-node .

### Running a Docker container

    $ docker run -ti danbev/fedora-node

### Building the Node RPM
Before running rpmbuild I needed to remove the `BuildRequirement` for scldev as it could not be found. This
requirement can be commented out by editing `nodejs.spec:

    #BuildRequires: %{?scl_prefix}scldevel

The run the following command to build the RPM:

    $ rpmbuild -ba nodejs.spec


### Delete old containers

    $ docker rm $(docker ps -a -q)


### RPM Spec file notes
A spec file is build up using RPM directives which have the following format:

    <tagname>:<value>

The tagname is not case sensitive.

A macro is defined using `%define`:

   %define macroname value

Then use the macro:

   %{macroname} or %macroname

Just note also that major sections in the spec file also use % but they are no
macros as they do not use the define keyword.

#### RPM build directories
This directory is created in `/root/rpmbuild` and has the following subdirectories:

* BUILD    this is where RPM builds the software
* RPMS     where the binary RPM are stored after being created
* SOURCES  where we place the sources
* SPECS    where spec file should be placed
* SRPMS    where the source RPM are stored after being created
