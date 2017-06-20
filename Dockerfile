FROM bucharestgold/rpmbuild-base:latest

RUN mkdir -p /usr/src/node-rpm
WORKDIR /usr/src/node-rpm/

COPY src/nodejs.spec src/nodejs-tarball.sh src/run.sh /usr/src/node-rpm/
COPY src/nodejs.spec /root/rpmbuild/SPECS

COPY src/patches/0002-Use-openssl-1.0.1.patch                          \
     src/patches/0003-CA-Certificates-are-provided-by-Fedora.patch     \
     src/patches/0004-Intl-test.patch                                  \
     src/patches/0005-Zlib-test.patch                                  \
     src/patches/0006-FIPS-test.patch                                  \
     src/nodejs_native.attr                                            \
     src/nodejs-tarball.sh /root/rpmbuild/SOURCES/

CMD ["./run.sh"]
