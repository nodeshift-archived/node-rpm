#!/bin/sh

echo "Building with version $VERSION"

## Get the Node distribution
wget http://nodejs.org/dist/v${VERSION}/node-v${VERSION}.tar.gz

## Remove openssl. Do we really need to do this?
tar -zxf node-v${VERSION}.tar.gz
rm -rf node-v${VERSION}/deps/openssl
tar -zcf node-v${VERSION}-stripped.tar.gz node-v${VERSION}

## Copy the stripped to to SOURCES
mv node-v${VERSION}-stripped.tar.gz /root/rpmbuild/SOURCES

## Build the rpm
rpmbuild -ba nodejs.spec

