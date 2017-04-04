#!/bin/sh

version=$(rpm -q --specfile --qf='%{version}\n' nodejs.spec | head -n1)
echo "Building with version $version"

## Get the Node distribution
wget http://nodejs.org/dist/v${version}/node-v${version}.tar.gz

## Remove openssl. Do we really need to do this?
tar -zxf node-v${version}.tar.gz
rm -rf node-v${version}/deps/openssl
tar -zcf node-v${version}-stripped.tar.gz node-v${version}

## Copy the stripped to to SOURCES
mv node-v${version}-stripped.tar.gz /root/rpmbuild/SOURCES

## Build the rpm
rpmbuild -ba nodejs.spec

