FROM bucharestgold/rhel-base

USER root

RUN mkdir -p /usr/src/node-rpm
RUN mkdir -p /root/rpmbuild_usr_src_debug
RUN git clone https://github.com/nodejs/node.git /root/rpmbuild_usr_src_debug/BUILD/nodejs
RUN echo "%_topdir /root/rpmbuild_usr_src_debug" > ~/.rpmmacros

WORKDIR /usr/src/node-rpm/

COPY src/nodejs.spec src/run.sh /usr/src/node-rpm/
COPY src/nodejs.spec /root/rpmbuild_usr_src_debug/SPECS/

COPY src/patches/0001-System-CA-Certificates.patch     \
     src/nodejs_native.attr /root/rpmbuild_usr_src_debug/SOURCES/

CMD ["./run.sh"]
