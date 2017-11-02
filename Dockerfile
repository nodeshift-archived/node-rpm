FROM openshift/base-centos7

RUN yum install -y rpmdevtools git gcc gcc-c++ openssl-devel libicu-devel python-devel systemtap-sdt-devel make

USER root
RUN mkdir -p /usr/src/node-rpm
WORKDIR /usr/src/node-rpm/

COPY nodejs.spec run.sh /usr/src/node-rpm/
COPY nodejs.spec /opt/app-root/src/rpmbuild/SPECS/

COPY 0001-System-CA-Certificates.patch     \
     license_xml.js                                \
     license_html.js                               \
     licenses.css                                  \
     nodejs_native.attr /opt/app-root/src/rpmbuild/SOURCES/

CMD ["./run.sh"]
