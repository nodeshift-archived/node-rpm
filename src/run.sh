#!/bin/sh

version=$(rpm -q --specfile --qf='%{version}\n' nodejs.spec | head -n1)
echo "Building with version $version"

pushd ../node
git checkout -fb ${version} v${version}
popd

tar -zcf node-v${version}.tar.gz --transform "s/^node/node-v${version}/" ../node

## Remove openssl. Do we really need to do this?
#tar -zxf node-v${version}.tar.gz
#rm -rf node-v${version}/deps/openssl
#tar -zcf node-v${version}-stripped.tar.gz node-v${version}

mv node-v${version}.tar.gz /root/rpmbuild/SOURCES

## Build the rpm
rpmbuild -ba nodejs.spec

