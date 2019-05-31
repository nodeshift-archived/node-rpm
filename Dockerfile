FROM registry.access.redhat.com/ubi8

COPY rpmdevtools/ /root/rpmdevtools/
RUN pushd /root/rpmdevtools && yum -y --nogpgcheck localinstall *.rpm && popd
RUN yum --skip-broken install -y git              \
                   gcc                            \
                   gcc-c++                        \
                   openssl-devel                  \
                   libicu-devel                   \
                   procps-ng                      \
                   python2-devel                  \
                   python3-devel                  \
                   systemtap-sdt-devel            \
                   platform-python-devel          \
                   make

RUN curl -L https://github.com/ccache/ccache/releases/download/v3.7.1/ccache-3.7.1.tar.bz2 --output ccache.tar.bz2 && \
    bzip2 -dc ccache.tar.bz2 | tar xvf - && \
    cd ccache-3.7.1/ && \
    ./configure && make && make install

USER root
WORKDIR /root/rpmbuild/SPECS/

COPY nodejs.spec run.sh create_node_tarball.sh /root/rpmbuild/SPECS/
COPY rsa.h /usr/include/openssl/

COPY license_xml.js                                            \
     license_html.js                                           \
     licenses.css                                              \
     nodejs_native.attr /root/rpmbuild/SOURCES/

CMD ["./run.sh"]
