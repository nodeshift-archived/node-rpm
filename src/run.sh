#!/bin/sh

version=$(rpm -q --specfile --qf='%{version}\n' nodejs.spec | head -n1)
echo "Building version $version"

curl -O http://nodejs.org/dist/v${version}/node-v${version}.tar.gz
mv node-v${version}.tar.gz /root/rpmbuild/SOURCES

## Build the rpm
rpmbuild -ba --noclean --define='basebuild 0' /usr/src/node-rpm/nodejs.spec
