FROM registry.access.redhat.com/ubi8

COPY rpmdevtools/ /root/rpmdevtools/
RUN pushd /root/rpmdevtools && yum -y --nogpgcheck localinstall *.rpm && popd
RUN yum install -y git                            \
                   gcc                            \
                   gcc-c++                        \
                   openssl-devel                  \
                   libicu-devel                   \
                   procps-ng                      \
                   python2-devel                  \
                   python3-devel                  \
                   systemtap-sdt-devel            \
                   make

USER root
WORKDIR /root/rpmbuild/SPECS/

COPY nodejs.spec run.sh create_node_tarball.sh /root/rpmbuild/SPECS/

COPY license_xml.js                                            \
     license_html.js                                           \
     licenses.css                                              \
     nodejs_native.attr /root/rpmbuild/SOURCES/

CMD ["./run.sh"]
