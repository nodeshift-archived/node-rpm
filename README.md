[![Build Status](https://travis-ci.org/bucharest-gold/node-rpm.svg?branch=master)](https://travis-ci.org/bucharest-gold/node-rpm)

### Node.js RPM Packaging
This purpose of this project is to create RPMs targeted for Fedora and RHEL to allow us to help identify issues
early and contribute changes upstream when possible.

The RPM [spec file](./src/nodejs.spec) was based on the spec file from this
[koji build](https://koji.fedoraproject.org/koji/buildinfo?buildID=861930).

### Releases 
Built releases are published on [github](https://github.com/bucharest-gold/node-rpm/releases).

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


### Node.js versions in Fedora/RHEL/CentOS


| OS Version | Package Node Version | SCL     |  EPEL     | Nodejs.org |
|------------|:--------------------:|--------:|----------:|:-----------|
| RHEL 7.3   | [N/A](#rhel-def)      | [v4.6.2](#rhel-scl)  |   [v6.10.1](#rhel-epel)     | [v7.9.0](#rhel-nodejsorg)    |
| Fedora 25  | [v6.10.0](#fedora-def)| [v4.6.2](#fedora-scl)  | [v6.10.0](#fedora-epel)   | [v7.9.0](#fedora-nodejsorg)    |
| CentOS  7  | [N/A](#centos-def)    | [v4.4.2](#centos-scl)  | [v6.10.0](#centos-epel)   | [v7.9.0](#centos-nodejsorg)    |

* Packaged in this case refers to having a repository preconfigured so that a direct install command using 
a package manager is possible, for example running `yum install -y nodejs` out of the box.

### Installing Node on RHEL

#### <a id="rhel-def"></a>Default packaged version

    $ docker pull registry.access.redhat.com/rhel7.3
    $ docker run -it registry.access.redhat.com/rhel7.3 bash
    $ subscription-manager register --username xxx --password xxx --auto-attach
    $ node -v
    $ yum install -y nodejs
    Loaded plugins: ovl, product-id, search-disabled-repos, subscription-manager
    No package nodejs available.
    Error: Nothing to do


#### <a id="rhel-scl"></a>Install Node using SCL

    $ docker run -it registry.access.redhat.com/rhel7.3 bash
    $ subscription-manager register --username xxx --password xxx --auto-attach
    $ yum-config-manager --enable rhel-server-rhscl-7-rpms
    $ yum install rh-nodejs4
    $ scl enable rh-nodejs4 bash
    $ node -v
    v4.6.2


#### <a id="rhel-epel"></a>Install Node using EPEL

    $ docker pull registry.access.redhat.com/rhel7.3
    $ docker run -it registry.access.redhat.com/rhel7.3 bash
    $ subscription-manager register --username xxx --password xxx --auto-attach
    $ rpm -Uvh http://ftp.acc.umu.se/mirror/fedora/epel/7/x86_64/e/epel-release-7-9.noarch.rpm
    $ yum install -y nodejs
    $ node -v
    v6.10.1

#### <a id="rhel-nodejsorg"></a>Install Node using nodejs.org

    $ docker run -it registry.access.redhat.com/rhel7.3 bash
    $ curl --silent --location https://rpm.nodesource.com/setup_7.x | bash -
    $ yum install -y nodejs
    $ node -v
    v7.9.0

----


### Installing Node on Fedora

#### <a id="fedora-def"></a>Default packaged version
  
    $ docker pull fedora
    $ docker run -it fedora bash
    $ dnf install nodejs
    $ node -v
    v6.10.0

#### <a id="fedora-scl"></a>Install Node using SCL
The [rh-nodejs4](https://www.softwarecollections.org/en/scls/rhscl/rh-nodejs4/) on the
Software Collections site only provides instructions for RHEL and CentOS.

#### <a id="fedora-epel"></a>Install Node using EPEL
Not applicable as EPEL is only for RHEL, CentOS, and Scientific Linux.


#### <a id="fedora-nodejsorg"></a>Install Node using nodejs.org

    $ docker run -it fedora bash
    $ curl --silent --location https://rpm.nodesource.com/setup_7.x | bash -
    $ yum install -y nodejs
    $ node -v
    v7.9.0

----

### Installing Node.js on CentOS

#### <a id="centos-def"></a>Default packaged version

    $ docker pull centos
    $ docker run -it centos bash
    $ yum install -y  nodejs
    No package nodejs available.
    Error: Nothing to do

#### <a id="centos-scl"></a>Install Node using SCL

    $ docker pull centos
    $ docker run -it centos bash
    $ yum install -y centos-release-scl
    $ yum install -y rh-nodejs4
    $ scl enable rh-nodejs4 bash
    $ node -v
    v4.4.2

#### <a id="centos-epel"></a>Install Node using EPEL

    $ docker pull centos
    $ docker run -it centos bash
    $ yum install epel-release
    $ yum install -y nodejs
    $ node -v
    v6.10.1

#### <a id="centos-nodejsorg"></a>Install Node using nodejs.org

    $ docker run -it centos bash
    $ curl --silent --location https://rpm.nodesource.com/setup_7.x | bash -
    $ yum install -y nodejs
    $ node -v
    v7.9.0

----

### List of packages installed with SCL

    $ docker run -it registry.access.redhat.com/rhel7.3 bash
    [root@468a8a25b34b /]# subscription-manager register --username xxx@redhat.com --password xxx --auto-attach
    [root@468a8a25b34b /]# yum-config-manager --enable rhel-server-rhscl-7-rpms
    [root@468a8a25b34b /]# yum install rh-nodejs4
    ==============================================================================================================================================
     Package                                                 Arch           Version                        Repository                        Size
    ==============================================================================================================================================
    Installing:
     rh-nodejs4                                              x86_64         2.2-5.el7                      rhel-server-rhscl-7-rpms         6.3 k
    Installing for dependencies:
     cpp                                                     x86_64         4.8.5-11.el7                   rhel-7-server-rpms               5.9 M
     gcc                                                     x86_64         4.8.5-11.el7                   rhel-7-server-rpms                16 M
     gcc-c++                                                 x86_64         4.8.5-11.el7                   rhel-7-server-rpms               7.2 M
     glibc-devel                                             x86_64         2.17-157.el7_3.1               rhel-7-server-rpms               1.1 M
     glibc-headers                                           x86_64         2.17-157.el7_3.1               rhel-7-server-rpms               668 k
     kernel-headers                                          x86_64         3.10.0-514.10.2.el7            rhel-7-server-rpms               4.8 M
     keyutils-libs-devel                                     x86_64         1.5.8-3.el7                    rhel-7-server-rpms                37 k
     krb5-devel                                              x86_64         1.14.1-27.el7_3                rhel-7-server-rpms               651 k
     libcom_err-devel                                        x86_64         1.42.9-9.el7                   rhel-7-server-rpms                31 k
     libgomp                                                 x86_64         4.8.5-11.el7                   rhel-7-server-rpms               152 k
     libkadm5                                                x86_64         1.14.1-27.el7_3                rhel-7-server-rpms               173 k
     libmpc                                                  x86_64         1.0.1-3.el7                    rhel-7-server-rpms                51 k
     libselinux-devel                                        x86_64         2.5-6.el7                      rhel-7-server-rpms               186 k
     libsepol-devel                                          x86_64         2.5-6.el7                      rhel-7-server-rpms                74 k
     libstdc++-devel                                         x86_64         4.8.5-11.el7                   rhel-7-server-rpms               1.5 M
     libverto-devel                                          x86_64         0.2.5-4.el7                    rhel-7-server-rpms                12 k
     make                                                    x86_64         1:3.82-23.el7                  rhel-7-server-rpms               421 k
     mpfr                                                    x86_64         3.1.1-4.el7                    rhel-7-server-rpms               203 k
     openssl                                                 x86_64         1:1.0.1e-60.el7_3.1            rhel-7-server-rpms               713 k
     openssl-devel                                           x86_64         1:1.0.1e-60.el7_3.1            rhel-7-server-rpms               1.2 M
     pcre-devel                                              x86_64         8.32-15.el7_2.1                rhel-7-server-rpms               479 k
     python-devel                                            x86_64         2.7.5-48.el7                   rhel-7-server-rpms               393 k
     rh-nodejs4-gyp                                          noarch         0.1-0.11.1617svn.el7           rhel-server-rhscl-7-rpms         404 k
     rh-nodejs4-http-parser                                  x86_64         2.7.0-2.el7                    rhel-server-rhscl-7-rpms          30 k
     rh-nodejs4-http-parser-devel                            x86_64         2.7.0-2.el7                    rhel-server-rhscl-7-rpms          11 k
     rh-nodejs4-libuv                                        x86_64         1:1.7.5-8.el7                  rhel-server-rhscl-7-rpms          72 k
     rh-nodejs4-libuv-devel                                  x86_64         1:1.7.5-8.el7                  rhel-server-rhscl-7-rpms          40 k
     rh-nodejs4-node-gyp                                     noarch         3.3.1-4.el7                    rhel-server-rhscl-7-rpms          33 k
     rh-nodejs4-nodejs                                       x86_64         4.6.2-4.el7                    rhel-server-rhscl-7-rpms         4.3 M
     rh-nodejs4-nodejs-abbrev                                noarch         1.0.7-2.el7                    rhel-server-rhscl-7-rpms         7.3 k
     rh-nodejs4-nodejs-ansi                                  noarch         0.3.0-3.el7                    rhel-server-rhscl-7-rpms          13 k
     rh-nodejs4-nodejs-ansi-regex                            noarch         2.0.0-5.el7                    rhel-server-rhscl-7-rpms         6.1 k
     rh-nodejs4-nodejs-ansicolors                            noarch         0.3.2-2.el7                    rhel-server-rhscl-7-rpms         6.5 k
     rh-nodejs4-nodejs-ansistyles                            noarch         0.1.3-4.el7                    rhel-server-rhscl-7-rpms         6.6 k
     rh-nodejs4-nodejs-archy                                 noarch         1.0.0-2.el7                    rhel-server-rhscl-7-rpms         6.7 k
     rh-nodejs4-nodejs-are-we-there-yet                      noarch         1.0.6-2.el7                    rhel-server-rhscl-7-rpms         8.8 k
     rh-nodejs4-nodejs-array-index                           noarch         0.1.1-4.el7                    rhel-server-rhscl-7-rpms         8.8 k
     rh-nodejs4-nodejs-asap                                  noarch         1.0.0-5.el7                    rhel-server-rhscl-7-rpms         7.8 k
     rh-nodejs4-nodejs-async-some                            noarch         1.0.2-3.el7                    rhel-server-rhscl-7-rpms         6.9 k
     rh-nodejs4-nodejs-balanced-match                        noarch         0.2.1-3.el7                    rhel-server-rhscl-7-rpms         6.8 k
     rh-nodejs4-nodejs-bl                                    noarch         1.0.0-2.el7                    rhel-server-rhscl-7-rpms          10 k
     rh-nodejs4-nodejs-block-stream                          noarch         0.0.8-1.el7                    rhel-server-rhscl-7-rpms         9.0 k
     rh-nodejs4-nodejs-brace-expansion                       noarch         1.1.1-3.el7                    rhel-server-rhscl-7-rpms         8.5 k
     rh-nodejs4-nodejs-builtin-modules                       noarch         1.1.1-4.el7                    rhel-server-rhscl-7-rpms         7.0 k
     rh-nodejs4-nodejs-builtins                              noarch         1.0.2-3.el7                    rhel-server-rhscl-7-rpms         5.6 k
     rh-nodejs4-nodejs-caseless                              noarch         0.11.0-2.el7                   rhel-server-rhscl-7-rpms         9.0 k
     rh-nodejs4-nodejs-char-spinner                          noarch         1.0.1-4.el7                    rhel-server-rhscl-7-rpms         6.1 k
     rh-nodejs4-nodejs-chmodr                                noarch         1.0.2-4.el7                    rhel-server-rhscl-7-rpms         6.1 k
     rh-nodejs4-nodejs-chownr                                noarch         1.0.1-4.el7                    rhel-server-rhscl-7-rpms         6.5 k
     rh-nodejs4-nodejs-clone                                 noarch         0.2.0-4.el7                    rhel-server-rhscl-7-rpms         8.3 k
     rh-nodejs4-nodejs-cmd-shim                              noarch         2.0.0-4.el7                    rhel-server-rhscl-7-rpms         8.5 k
     rh-nodejs4-nodejs-columnify                             noarch         1.5.4-1.el7                    rhel-server-rhscl-7-rpms          14 k
     rh-nodejs4-nodejs-concat-map                            noarch         0.0.1-3.el7                    rhel-server-rhscl-7-rpms         6.0 k
     rh-nodejs4-nodejs-concat-stream                         noarch         1.4.4-6.el7                    rhel-server-rhscl-7-rpms         7.9 k
     rh-nodejs4-nodejs-config-chain                          noarch         1.1.9-2.el7                    rhel-server-rhscl-7-rpms          11 k
     rh-nodejs4-nodejs-core-util-is                          noarch         1.0.2-3.el7                    rhel-server-rhscl-7-rpms         6.2 k
     rh-nodejs4-nodejs-debug                                 noarch         2.2.0-4.el7                    rhel-server-rhscl-7-rpms          15 k
     rh-nodejs4-nodejs-debuglog                              noarch         1.0.1-5.el7                    rhel-server-rhscl-7-rpms         6.2 k
     rh-nodejs4-nodejs-defaults                              noarch         1.0.0-7.el7                    rhel-server-rhscl-7-rpms         5.4 k
     rh-nodejs4-nodejs-delegates                             noarch         0.1.0-3.el7                    rhel-server-rhscl-7-rpms         5.5 k
     rh-nodejs4-nodejs-devel                                 x86_64         4.6.2-4.el7                    rhel-server-rhscl-7-rpms         4.6 M
     rh-nodejs4-nodejs-dezalgo                               noarch         1.0.2-4.el7                    rhel-server-rhscl-7-rpms         7.5 k
     rh-nodejs4-nodejs-editor                                noarch         1.0.0-2.el7                    rhel-server-rhscl-7-rpms         6.8 k
     rh-nodejs4-nodejs-forever-agent                         noarch         0.5.0-4.el7                    rhel-server-rhscl-7-rpms         9.5 k
     rh-nodejs4-nodejs-fs-vacuum                             noarch         1.2.6-4.el7                    rhel-server-rhscl-7-rpms         7.3 k
     rh-nodejs4-nodejs-fs-write-stream-atomic                noarch         1.0.3-4.el7                    rhel-server-rhscl-7-rpms         7.1 k
     rh-nodejs4-nodejs-fstream                               noarch         1.0.3-3.el7                    rhel-server-rhscl-7-rpms          25 k
     rh-nodejs4-nodejs-fstream-ignore                        noarch         1.0.2-4.el7                    rhel-server-rhscl-7-rpms          10 k
     rh-nodejs4-nodejs-fstream-npm                           noarch         1.0.7-2.el7                    rhel-server-rhscl-7-rpms          12 k
     rh-nodejs4-nodejs-gauge                                 noarch         1.2.2-6.el7                    rhel-server-rhscl-7-rpms          10 k
     rh-nodejs4-nodejs-github-url-from-git                   noarch         1.4.0-2.el7                    rhel-server-rhscl-7-rpms         6.6 k
     rh-nodejs4-nodejs-github-url-from-username-repo         noarch         1.0.2-1.el7                    rhel-server-rhscl-7-rpms         6.1 k
     rh-nodejs4-nodejs-glob                                  noarch         7.0.3-1.el7                    rhel-server-rhscl-7-rpms          21 k
     rh-nodejs4-nodejs-graceful-fs                           noarch         4.1.2-4.el7                    rhel-server-rhscl-7-rpms          13 k
     rh-nodejs4-nodejs-has-unicode                           noarch         2.0.0-3.el7                    rhel-server-rhscl-7-rpms         6.1 k
     rh-nodejs4-nodejs-hosted-git-info                       noarch         2.1.4-4.el7                    rhel-server-rhscl-7-rpms         9.2 k
     rh-nodejs4-nodejs-imurmurhash                           noarch         0.1.4-1.el7                    rhel-server-rhscl-7-rpms         8.3 k
     rh-nodejs4-nodejs-inflight                              noarch         1.0.4-3.el7                    rhel-server-rhscl-7-rpms         6.4 k
     rh-nodejs4-nodejs-inherits                              noarch         2.0.0-15.el7                   rhel-server-rhscl-7-rpms         9.4 k
     rh-nodejs4-nodejs-ini                                   noarch         1.3.4-2.el7                    rhel-server-rhscl-7-rpms         8.8 k
     rh-nodejs4-nodejs-init-package-json                     noarch         1.9.3-1.el7                    rhel-server-rhscl-7-rpms          13 k
     rh-nodejs4-nodejs-is-absolute                           noarch         0.2.3-4.el7                    rhel-server-rhscl-7-rpms         6.8 k
     rh-nodejs4-nodejs-is-builtin-module                     noarch         1.0.0-2.el7                    rhel-server-rhscl-7-rpms         6.1 k
     rh-nodejs4-nodejs-is-relative                           noarch         0.2.1-4.el7                    rhel-server-rhscl-7-rpms         6.3 k
     rh-nodejs4-nodejs-is-unc-path                           noarch         0.1.1-4.el7                    rhel-server-rhscl-7-rpms         6.6 k
     rh-nodejs4-nodejs-is-windows                            noarch         0.1.0-4.el7                    rhel-server-rhscl-7-rpms         6.1 k
     rh-nodejs4-nodejs-isarray                               noarch         0.0.1-5.el7                    rhel-server-rhscl-7-rpms         7.1 k
     rh-nodejs4-nodejs-jju                                   noarch         1.2.1-4.el7                    rhel-server-rhscl-7-rpms         8.1 k
     rh-nodejs4-nodejs-json-parse-helpfulerror               noarch         1.0.3-2.el7                    rhel-server-rhscl-7-rpms         6.2 k
     rh-nodejs4-nodejs-json-stringify-safe                   noarch         5.0.0-3.el7                    rhel-server-rhscl-7-rpms         6.8 k
     rh-nodejs4-nodejs-lockfile                              noarch         1.0.1-3.el7                    rhel-server-rhscl-7-rpms          13 k
     rh-nodejs4-nodejs-lodash._basetostring                  noarch         3.0.1-3.el7                    rhel-server-rhscl-7-rpms         6.1 k
     rh-nodejs4-nodejs-lodash._createpadding                 noarch         3.6.1-2.el7                    rhel-server-rhscl-7-rpms         6.6 k
     rh-nodejs4-nodejs-lodash.pad                            noarch         3.1.1-1.el7                    rhel-server-rhscl-7-rpms         6.9 k
     rh-nodejs4-nodejs-lodash.padleft                        noarch         3.1.1-3.el7                    rhel-server-rhscl-7-rpms         7.0 k
     rh-nodejs4-nodejs-lodash.padright                       noarch         3.1.1-2.el7                    rhel-server-rhscl-7-rpms         7.0 k
     rh-nodejs4-nodejs-lodash.repeat                         noarch         3.0.1-3.el7                    rhel-server-rhscl-7-rpms         6.8 k
     rh-nodejs4-nodejs-lru-cache                             noarch         3.2.0-2.el7                    rhel-server-rhscl-7-rpms          11 k
     rh-nodejs4-nodejs-mime-db                               noarch         1.15.0-4.el7                   rhel-server-rhscl-7-rpms          23 k
     rh-nodejs4-nodejs-mime-types                            noarch         2.1.3-2.el7                    rhel-server-rhscl-7-rpms         7.9 k
     rh-nodejs4-nodejs-minimatch                             noarch         3.0.2-1.el7                    rhel-server-rhscl-7-rpms          17 k
     rh-nodejs4-nodejs-minimist                              noarch         0.0.8-2.el7                    rhel-server-rhscl-7-rpms         8.0 k
     rh-nodejs4-nodejs-mkdirp                                noarch         0.5.0-2.el7                    rhel-server-rhscl-7-rpms         8.3 k
     rh-nodejs4-nodejs-ms                                    noarch         0.7.1-4.el7                    rhel-server-rhscl-7-rpms         8.0 k
     rh-nodejs4-nodejs-mute-stream                           noarch         0.0.4-4.el7                    rhel-server-rhscl-7-rpms         7.8 k
     rh-nodejs4-nodejs-node-uuid                             noarch         1.4.1-3.el7                    rhel-server-rhscl-7-rpms          10 k
     rh-nodejs4-nodejs-nopt                                  noarch         3.0.6-3.el7                    rhel-server-rhscl-7-rpms          14 k
     rh-nodejs4-nodejs-normalize-git-url                     noarch         3.0.1-2.el7                    rhel-server-rhscl-7-rpms         6.7 k
     rh-nodejs4-nodejs-normalize-package-data                noarch         2.3.5-2.el7                    rhel-server-rhscl-7-rpms          15 k
     rh-nodejs4-nodejs-npm-cache-filename                    noarch         1.0.2-2.el7                    rhel-server-rhscl-7-rpms         5.8 k
     rh-nodejs4-nodejs-npm-install-checks                    noarch         1.0.6-2.el7                    rhel-server-rhscl-7-rpms         7.7 k
     rh-nodejs4-nodejs-npm-package-arg                       noarch         4.1.0-2.el7                    rhel-server-rhscl-7-rpms         8.9 k
     rh-nodejs4-nodejs-npm-registry-client                   noarch         7.1.0-1.el7                    rhel-server-rhscl-7-rpms          26 k
     rh-nodejs4-nodejs-npm-user-validate                     noarch         0.1.1-2.el7                    rhel-server-rhscl-7-rpms         6.4 k
     rh-nodejs4-nodejs-npmlog                                noarch         2.0.0-3.el7                    rhel-server-rhscl-7-rpms          11 k
     rh-nodejs4-nodejs-once                                  noarch         1.3.3-2.el7                    rhel-server-rhscl-7-rpms         6.5 k
     rh-nodejs4-nodejs-opener                                noarch         1.4.1-2.el7                    rhel-server-rhscl-7-rpms         7.4 k
     rh-nodejs4-nodejs-os-homedir                            noarch         1.0.1-2.el7                    rhel-server-rhscl-7-rpms         5.8 k
     rh-nodejs4-nodejs-os-tmpdir                             noarch         1.0.1-4.el7                    rhel-server-rhscl-7-rpms         5.9 k
     rh-nodejs4-nodejs-osenv                                 noarch         0.1.3-3.el7                    rhel-server-rhscl-7-rpms         7.6 k
     rh-nodejs4-nodejs-path-array                            noarch         1.0.0-2.el7                    rhel-server-rhscl-7-rpms         7.1 k
     rh-nodejs4-nodejs-path-is-absolute                      noarch         1.0.0-2.el7                    rhel-server-rhscl-7-rpms         5.9 k
     rh-nodejs4-nodejs-path-is-inside                        noarch         1.0.1-1.el7                    rhel-server-rhscl-7-rpms         6.3 k
     rh-nodejs4-nodejs-process-nextick-args                  noarch         1.0.2-3.el7                    rhel-server-rhscl-7-rpms         5.8 k
     rh-nodejs4-nodejs-promzard                              noarch         0.3.0-3.el7                    rhel-server-rhscl-7-rpms          13 k
     rh-nodejs4-nodejs-proto-list                            noarch         1.2.2-6.el7                    rhel-server-rhscl-7-rpms         6.7 k
     rh-nodejs4-nodejs-pseudomap                             noarch         1.0.2-1.el7                    rhel-server-rhscl-7-rpms         7.3 k
     rh-nodejs4-nodejs-qs                                    noarch         1.2.2-2.el7                    rhel-server-rhscl-7-rpms          11 k
     rh-nodejs4-nodejs-read                                  noarch         1.0.5-2.el7                    rhel-server-rhscl-7-rpms         8.9 k
     rh-nodejs4-nodejs-read-installed                        noarch         4.0.3-2.el7                    rhel-server-rhscl-7-rpms          11 k
     rh-nodejs4-nodejs-read-package-json                     noarch         2.0.3-1.el7                    rhel-server-rhscl-7-rpms          12 k
     rh-nodejs4-nodejs-readable-stream                       noarch         2.0.2-6.el7                    rhel-server-rhscl-7-rpms          22 k
     rh-nodejs4-nodejs-readdir-scoped-modules                noarch         1.0.2-2.el7                    rhel-server-rhscl-7-rpms         7.0 k
     rh-nodejs4-nodejs-realize-package-specifier             noarch         3.0.1-2.el7                    rhel-server-rhscl-7-rpms         7.5 k
     rh-nodejs4-nodejs-request                               noarch         2.42.0-7.el7                   rhel-server-rhscl-7-rpms          33 k
     rh-nodejs4-nodejs-retry                                 noarch         0.9.0-1.el7                    rhel-server-rhscl-7-rpms          12 k
     rh-nodejs4-nodejs-rimraf                                noarch         2.5.2-2.el7                    rhel-server-rhscl-7-rpms          11 k
     rh-nodejs4-nodejs-semver                                noarch         5.1.0-2.el7                    rhel-server-rhscl-7-rpms          20 k
     rh-nodejs4-nodejs-sha                                   noarch         2.0.1-3.1.el7                  rhel-server-rhscl-7-rpms         8.0 k
     rh-nodejs4-nodejs-slide                                 noarch         1.1.6-2.el7                    rhel-server-rhscl-7-rpms          10 k
     rh-nodejs4-nodejs-sorted-object                         noarch         1.0.0-5.el7                    rhel-server-rhscl-7-rpms         6.6 k
     rh-nodejs4-nodejs-spdx-correct                          noarch         1.0.2-2.el7                    rhel-server-rhscl-7-rpms         9.6 k
     rh-nodejs4-nodejs-spdx-exceptions                       noarch         1.0.4-3.el7                    rhel-server-rhscl-7-rpms         5.1 k
     rh-nodejs4-nodejs-spdx-expression-parse                 noarch         1.0.2-2.el7                    rhel-server-rhscl-7-rpms          13 k
     rh-nodejs4-nodejs-spdx-license-ids                      noarch         1.2.0-1.el7                    rhel-server-rhscl-7-rpms         9.2 k
     rh-nodejs4-nodejs-string_decoder                        noarch         0.10.31-3.el7                  rhel-server-rhscl-7-rpms         7.6 k
     rh-nodejs4-nodejs-strip-ansi                            noarch         3.0.0-2.el7                    rhel-server-rhscl-7-rpms         6.5 k
     rh-nodejs4-nodejs-tar                                   noarch         2.2.1-3.el7                    rhel-server-rhscl-7-rpms          23 k
     rh-nodejs4-nodejs-text-table                            noarch         0.2.0-3.el7                    rhel-server-rhscl-7-rpms         6.9 k
     rh-nodejs4-nodejs-tunnel-agent                          noarch         0.4.3-1.el7                    rhel-server-rhscl-7-rpms          10 k
     rh-nodejs4-nodejs-uid-number                            noarch         0.0.5-3.el7                    rhel-server-rhscl-7-rpms         7.1 k
     rh-nodejs4-nodejs-umask                                 noarch         1.1.0-5.el7                    rhel-server-rhscl-7-rpms         6.9 k
     rh-nodejs4-nodejs-unc-path-regex                        noarch         0.1.1-3.el7                    rhel-server-rhscl-7-rpms         6.4 k
     rh-nodejs4-nodejs-util-deprecate                        noarch         1.0.1-3.el7                    rhel-server-rhscl-7-rpms         6.3 k
     rh-nodejs4-nodejs-util-extend                           noarch         1.0.1-8.el7                    rhel-server-rhscl-7-rpms         6.1 k
     rh-nodejs4-nodejs-validate-npm-package-license          noarch         3.0.1-2.el7                    rhel-server-rhscl-7-rpms          10 k
     rh-nodejs4-nodejs-validate-npm-package-name             noarch         2.2.2-4.el7                    rhel-server-rhscl-7-rpms         7.5 k
     rh-nodejs4-nodejs-wcwidth                               noarch         1.0.0-7.el7                    rhel-server-rhscl-7-rpms         9.8 k
     rh-nodejs4-nodejs-which                                 noarch         1.2.0-5.el7                    rhel-server-rhscl-7-rpms         9.1 k
     rh-nodejs4-nodejs-wrappy                                noarch         1.0.1-3.el7                    rhel-server-rhscl-7-rpms         5.7 k
     rh-nodejs4-nodejs-write-file-atomic                     noarch         1.1.2-4.el7                    rhel-server-rhscl-7-rpms         7.1 k
     rh-nodejs4-npm                                          noarch         2.15.1-8.el7                   rhel-server-rhscl-7-rpms         495 k
     rh-nodejs4-runtime                                      x86_64         2.2-5.el7                      rhel-server-rhscl-7-rpms         1.1 M
     scl-utils                                               x86_64         20130529-17.el7_1              rhel-7-server-rpms                24 k
     zlib-devel                                              x86_64         1.2.7-17.el7                   rhel-7-server-rpms                50 k

    Transaction Summary
    ==============================================================================================================================================
    Install  1 Package (+165 Dependent packages)

    Total download size: 54 M
    Installed size: 134 M
    Is this ok [y/d/N]:y
    ...
    [root@468a8a25b34b /]# scl enable rh-nodejs4 bash
    [root@468a8a25b34b /]# node -v
    v4.6.2

From the above output you can see all the packages that get installed plus how to use the scl tool to enable rh-nodejs4 in a
new process running bash.


### Creating a new base image
A new base image can be created by updating the image in (DockerFile](./Dockerfile) to `fedora` and then following the
sections below.

#### Install packages
These are packages that we installed to build Node.js and are required to be installed when creating a new base image.

    $ dnf install -y git
    $ dnf install -y rpmdevtools
    $ dnf install -y procps-ng
    $ dnf install -y gcc gcc-c++ openssl-devel libicu-devel python-devel systemtap-sdt-devel zlib-devel libuv-devel
    $ dnf clean all

### Configuration

#### Configure the rpmbuild `_topdir`

    $ echo "%_topdir /root/rpmbuild_usr_src_debug" > ~/.rpmmacros

#### Checkout node.js

    $ cd /root/rpmbuild_usr_src_debug/
    $ mkdir BUILD
    $ cd BUILD
    $ git clone https://github.com/nodejs/node nodejs

####  Build Node
    $ cd /usr/src/node-rpm
    $ ./build-base-image.sh

It is possible that the above build will fail while running test but that is not important at this stage. When we
run the real rpm build there will be a patching stage which will patch any failing tests. The only goal here
is to compile to save time.


#### Commit and push the image

    $ docker commit -a "Daniel Bevenius <daniel.bevenius@gmail.com>" -m "Base Image for building Node.js 8.1.0" 68b03eeff1df bucharestgold/rpmbuild-base-8-1-0
    $ docker tag bucharestgold/rpmbuild-base-8-1-0 bucharestgold/rpmbuild-base:8.1.0
    $ docker login
    $ docker push bucharestgold/rpmbuild-base:8.1.0
    
