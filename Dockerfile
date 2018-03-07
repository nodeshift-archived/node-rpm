FROM openshift/base-centos7

RUN yum install -y rpmdevtools         \
                   git gcc gcc-c++     \
                   openssl-devel       \
                   libicu-devel        \
                   python-devel        \
                   systemtap-sdt-devel \
                   make

USER root
WORKDIR /opt/app-root/src/rpmbuild/SPECS/

COPY nodejs.spec run.sh create_node_tarball.sh /opt/app-root/src/rpmbuild/SPECS/

COPY license_xml.js                                            \
     license_html.js                                           \
     licenses.css                                              \
     0001-test-tls-cnnic-whitlist.patch                        \
     0002-test-child-process-spawnsync-validation-errors.patch \
     nodejs_native.attr /opt/app-root/src/rpmbuild/SOURCES/

CMD ["./run.sh"]
