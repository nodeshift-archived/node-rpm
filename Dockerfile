FROM openshift/base-centos7

RUN yum install -y rpmdevtools         \
                   git devtoolset-7-gcc devtoolset-7-gcc-c++     \
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
     nodejs_native.attr /opt/app-root/src/rpmbuild/SOURCES/

CMD ["./run.sh"]
