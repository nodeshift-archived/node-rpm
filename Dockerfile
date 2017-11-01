FROM bucharestgold/rhel-base

USER root
RUN mkdir -p /usr/src/node-rpm
WORKDIR /usr/src/node-rpm/

COPY nodejs.spec run.sh /usr/src/node-rpm/
COPY nodejs.spec /root/rpmbuild/SPECS/

COPY 0001-System-CA-Certificates.patch     \
     license_xml.js                                \
     license_html.js                               \
     licenses.css                                  \
     nodejs_native.attr /root/rpmbuild/SOURCES/

CMD ["./run.sh"]
