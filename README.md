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

#### Why are only the parallel test run
Currentl only the parallel test are run and nothing else:

    python tools/test.py --mode=release parallel -J

This will miss the cctest and addons for example. Perhaps this is done as they
are currently failing for them but hopefully in the future this could be update
to run the full suite of tests. 



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
