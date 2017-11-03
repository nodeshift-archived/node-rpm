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

COPY 0001-System-CA-Certificates.patch             \
     0002-Internet.patch                           \
     license_xml.js                                \
     license_html.js                               \
     licenses.css                                  \
     nodejs_native.attr /opt/app-root/src/rpmbuild/SOURCES/

CMD ["./run.sh"]
