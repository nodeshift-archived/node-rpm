FROM openshift/base-centos7

RUN yum install -y centos-release-scl  && \
    yum remove -y  gcc                 && \
    yum install -y devtoolset-7-gcc devtoolset-7-gcc-c++  && \
    yum install -y rpmdevtools            \
                   git                    \
                   openssl-devel          \
                   libicu-devel           \
                   python-devel           \
                   systemtap-sdt-devel    \
                   make              

ENV PATH $PATH:/opt/rh/devtoolset-7/root/usr/bin

USER root
WORKDIR /opt/app-root/src/rpmbuild/SPECS/

COPY nodejs.spec run.sh create_node_tarball.sh /opt/app-root/src/rpmbuild/SPECS/

COPY license_xml.js                                            \
     license_html.js                                           \
     licenses.css                                              \
     test-fs-copy.patch                                        \
     nodejs_native.attr /opt/app-root/src/rpmbuild/SOURCES/

CMD ["./run.sh"]
