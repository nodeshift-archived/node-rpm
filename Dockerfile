FROM bucharestgold/rpmbuild-base:8.3.0

RUN mkdir -p /usr/src/node-rpm
WORKDIR /usr/src/node-rpm/

COPY src/nodejs.spec src/nodejs-tarball.sh src/run.sh src/build-base-image.sh /usr/src/node-rpm/
COPY src/nodejs.spec /root/rpmbuild_usr_src_debug/SPECS/

COPY src/patches/0002-Use-openssl-1.0.1.patch                          \
     src/patches/0003-CA-Certificates-are-provided-by-Fedora.patch     \
     src/nodejs_native.attr                                            \
     src/nodejs-tarball.sh /root/rpmbuild_usr_src_debug/SOURCES/

CMD ["./run.sh"]
