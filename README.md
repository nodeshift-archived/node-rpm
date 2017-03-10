[![Build Status](https://travis-ci.org/danbev/node-rpm.svg?branch=master)](https://travis-ci.org/danbev/node-rpm)

### RHEL Node.js RPM Packaging image
This project exist to help me understand how Node.js is packaged as an RPM by Fedora/RHEL.

### Increase memory limit
When runnnig the build you may require more than the default 2GB or memory.
This can be done by increasing the memory limit in Docker for Mac preferences.
If you see an error similar to this you may need to increase your memory settings:

    collect2: fatal error: ld terminated with signal 9 [Killed]

### Building the Docker image

    $ docker build -t danbev/fedora-node .

### Running a Docker container

    $ docker run -ti --env VERSION=6.9.1 danbev/fedora-node

### Building the Node RPM
Before running rpmbuild I needed to remove the `BuildRequirement` for scldev as it could not be found. This
requirement can be commented out by editing `nodejs.spec:

    #BuildRequires: %{?scl_prefix}scldevel

The run the following command to build the RPM:

    $ rpmbuild -ba nodejs.spec

If all goes well you should see the following output:

    Wrote: /root/rpmbuild/SRPMS/nodejs-6.9.1-2.fc25.src.rpm
    Wrote: /root/rpmbuild/RPMS/x86_64/nodejs-6.9.1-2.fc25.x86_64.rpm
    Wrote: /root/rpmbuild/RPMS/x86_64/nodejs-devel-6.9.1-2.fc25.x86_64.rpm
    Wrote: /root/rpmbuild/RPMS/noarch/nodejs-docs-6.9.1-2.fc25.noarch.rpm
    Wrote: /root/rpmbuild/RPMS/x86_64/nodejs-debuginfo-6.9.1-2.fc25.x86_64.rpm


Copy a RPM form the container:

    $ docker cp <containerId>:/root/rpmbuild/RPMS/x86_64/nodejs-6.9.1-2.fc25.x86_64.rpm .


### Delete old containers

    $ docker rm $(docker ps -a -q)


### Questions

#### Does openssl need to be removed from the downloaded tar?
Currently the nodejs-tarball.sh downloads the Node.js version specified in the 
spec file and then removed `dep/openssl` from it. Perhaps it would be enough
to just configure `--without-ssl` and not remove it. Is this so that it does not
end up in the source rpm file?

    $ rpm -qpl ~/rpmbuild/SRPMS/nodejs-6.9.1-2.fc25.src.rpm
    0001-Disable-crypto-tests.patch
    0001-Disable-failing-tests.patch
    0002-Use-openssl-1.0.1.patch
    node-v6.9.1-stripped.tar.gz
    nodejs-disable-gyp-deps.patch
    nodejs-tarball.sh
    nodejs-use-system-certs.patch
    nodejs.spec

#### Why are only the parallel test run?
Currentl only the parallel test are run and nothing else:

    python tools/test.py --mode=release parallel -J

This will miss the cctest and addons for example. Some of these test depend on `npm` which
has been removed from the deps directory which would explain why those test are not being
executed. 

#### Does npm really need to be removed?
It looks like npm is removed to avoid it from being installed on the target system, but
this is accomplished using the `--without-npm`flag which is already specified.
If needed deps/npm could be removed after as the last step in the checks section.


#### Disabled tests
`test/parallel/npm-install.js` fails because npm in removed. In upstream there is a check 
added to see if crypto is installed, and if not this test will be skipped. So this test
could be enabled at some point. Also there is a configuration option `--without-npm` that 
migth be usable. This seems to be because the test are dependant on the deps/npm which 
has been removed. But I'm not sure why the deps is removed from the source
tree. It looks like we can avoid installing this using the `--without-npm` and then still 
be able to run the tests

`test-net-connect-immediate-finish.js`passes for me. Need to find out the what differences
there might be compared to the target environment this is normally run on.

`test-net-better-error-messages-port-hostname.js`


#### Is scldevel really needed?
This seems to build fine without this build requirement, is it really needed?

#### Suggestion
This repository could be reponsible for creating RPMs for Node [distributions](http://nodejs.org/dist) and 
publishing the RPMs as github releases. Travis CI would be responsible for building the RPMs and publishing.

This would allow us to take responsibility for the RPM creation and fix any new issue identified that concern
Node.js source code changes. 
If we can also find out what additional tests are run on an RPM we might be able to extend CI execution to 
include them before publishing the final RPM.

Development process:
* For each major version of Node.js a branch in this repo will exist for it
* For any minor/patch release a branch will be created for it and pushed for Travis CI to run (with out publishing)
* If CI fails then manual building using Docker can be done to identify the issue and fix
* When CI completes a tag is created for the minor/patch version and published

_____

### nodjs.spec walkthrough/notes
A spec file is build up using RPM directives which have the following format:

    <tagname>:<value>

The tagname is not case sensitive.

A macro is defined using `%define`:

   %define macroname value

Then use the macro:

   %{macroname} or %macroname

Just note also that major sections in the spec file also use % but they are no
macros as they do not use the define keyword.

Pathes are listed using:

    Patch1: nodejs-disable-gyp-deps.patch

And then applied using the patch directive `%patch':

    %patch1 -p1

Preparing the build process is used with the %prep directive:

    %prep
    %setup -q -n node-v%{version}

The setup command changes to /root/rpmbuild directory and extracts the source code.

The `-q` is to make it quit and `-n` to name the directory (of the extracted source)
which in our case will be `~/rpmbuild/BUILD/node-v6.9.1/`
After this the patches are applied and then the deps that are not used 'nvm', 'libuv', 'http-parser', and 'zlib' are removed:

    $ rm -rf deps/npm \
       deps/uv \
       deps/http-parser \
       deps/zlib

src/node_root_certs.h is also removed from the sources after patch2 has been applied.

The `%build` section does the actual build prepared in the `%prep` section.
Apart from setting compiler flags the normal configure is found:

    $ ./configure --prefix=%{_prefix} \
           --shared-http-parser \
           --shared-zlib \
           --shared-libuv \
           --without-npm \
           --without-dtrace \
           --shared-openssl

Then make is run specifying a `BUILDTYPE` of Debug or Release:

    $ make BUILDTYPE=Release|Debug

Next, the %install section installs the software:

    %install
    ./tools/install.py install %{buildroot} %{_prefix}

The `%check` section currently only run the parallel tests:

    %check
    %{?scl:scl enable %{scl} "}
    python tools/test.py --mode=release parallel -J
    %{?scl:"}

This will miss the cctest and addons for example. Perhaps this is done as they
are currently failing for them but hopefully in the future this could be update
to run the full suite of tests.

The `%files` section specifies all the files that should be installed from this
package.


#### RPM build directories
This directory is created in `/root/rpmbuild` and has the following subdirectories:

* BUILD      this is where RPM builds node
* RPMS       where the binary RPM are stored after being created
* SOURCES    where we place the sources
* SPECS      where spec file should be placed
* SRPMS      where the source RPM are stored after being created
* BUILDROOT  a staging area that looks like the final installation directory
