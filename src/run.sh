#!/bin/sh

version=$(rpm -q --specfile --qf='%{version}\n' nodejs.spec | head -n1)
echo "Building version $version"

curl -O http://nodejs.org/dist/v${version}/node-v${version}.tar.gz
tar -zxf node-v${version}.tar.gz
rm -rf node-v${version}/deps/openssl
tar -zcf node-v${version}-stripped.tar.gz node-v${version}
mv node-v${version}-stripped.tar.gz /root/rpmbuild/SOURCES/node-v${version}.tar.gz

## Build the rpm
rpmbuild -ba --noclean --define='basebuild 0' /usr/src/node-rpm/nodejs.spec
