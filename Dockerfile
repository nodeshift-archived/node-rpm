FROM fedora:latest

RUN yum install -y @development-tools
RUN yum install -y fedora-packager
RUN yum install -y gcc-c++ gyp http-parser-devel libuv-devel openssl-devel procps-ng python-devel zlib-devel wget

RUN rpmdev-setuptree

RUN mkdir -p /usr/src/node-rpm
WORKDIR /usr/src/node-rpm/

COPY src/nodejs.spec src/nodejs-tarball.sh /usr/src/node-rpm/
COPY src/nodejs.spec /root/rpmbuild/SPEC

COPY src/patches/0001-Disable-crypto-tests.patch   \
     src/patches/0001-Disable-failing-tests.patch  \
     src/patches/0002-Use-openssl-1.0.1.patch      \
     src/patches/nodejs-disable-gyp-deps.patch     \
     src/patches/nodejs-use-system-certs.patch     \
     src/nodejs-tarball.sh /root/rpmbuild/SOURCES/ 

RUN /usr/src/node-rpm/nodejs-tarball.sh
RUN cp /usr/src/node-rpm/*.tar.gz /root/rpmbuild/SOURCES/
CMD ["bash"]
