FROM nodeshift/node12-base:12.1.0

ENV PATH $PATH:/opt/rh/devtoolset-7/root/usr/bin

USER root
WORKDIR /opt/app-root/src/rpmbuild/SPECS/

COPY nodejs.spec run.sh /opt/app-root/src/rpmbuild/SPECS/

COPY license_xml.js                                            \
     license_html.js                                           \
     licenses.css                                              \
     test-fs-copy.patch                                        \
     nodejs_native.attr /opt/app-root/src/rpmbuild/SOURCES/

CMD ["./run.sh"]
