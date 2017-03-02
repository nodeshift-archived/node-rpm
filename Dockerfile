FROM fedora:latest

RUN yum install -y @development-tools
RUN yum install -y fedora-packager
RUN yum install -y gcc-c++ gyp http-parser-devel libuv-devel openssl-devel procps-ng python-devel zlib-devel wget

RUN rpmdev-setuptree

RUN mkdir -p /usr/src/node-rhel
WORKDIR /usr/src/node-rhel/

COPY rpm-repo/nodejs.spec rpm-repo/nodejs-tarball.sh /usr/src/node-rhel/

COPY rpm-repo/0001-Disable-crypto-tests.patch   \
     rpm-repo/0001-Disable-failing-tests.patch  \
     rpm-repo/0002-Use-openssl-1.0.1.patch      \
     rpm-repo/nodejs-disable-gyp-deps.patch     \
     rpm-repo/nodejs-tarball.sh                 \
     rpm-repo/nodejs-use-system-certs.patch     \
     rpm-repo/sources /root/rpmbuild/SOURCES/

RUN /usr/src/node-rhel/nodejs-tarball.sh
RUN cp /usr/src/node-rhel/*.tar.gz /root/rpmbuild/SOURCES/
CMD ["bash"]
