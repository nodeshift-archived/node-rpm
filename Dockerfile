FROM fedora:latest

RUN yum install -y @development-tools
RUN yum install -y fedora-packager
RUN yum install -y gcc-c++                                              \
                   gyp                                                  \
                   http-parser-devel                                    \
                   libuv-devel                                          \
                   openssl-devel                                        \
                   libicu-devel                                         \
                   procps-ng                                            \
                   python-devel                                         \
                   zlib-devel                                           \
                   wget 

RUN rpmdev-setuptree

RUN mkdir -p /usr/src/node-rpm
WORKDIR /usr/src/node-rpm/

COPY src/nodejs.spec src/nodejs-tarball.sh src/run.sh /usr/src/node-rpm/
COPY src/nodejs.spec /root/rpmbuild/SPECS

COPY src/patches/0001-disable-running-gyp-files-for-bundled-deps.patch \
     src/patches/0002-Use-openssl-1.0.1.patch                          \
     src/patches/0002-Use-openssl-1.0.1.patch                          \
     src/patches/0003-CA-Certificates-are-provided-by-Fedora.patch     \
     src/nodejs-tarball.sh /root/rpmbuild/SOURCES/

CMD ["./run.sh"]
