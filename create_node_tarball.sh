#!/bin/sh

version=$(rpm -q --specfile --qf='%{version}\n' nodejs.spec | head -n1)
node_version=node-v${version}-rh

git clone https://github.com/bucharest-gold/node.git -b v${version}-rh ${node_version}

## Download the FIPS Module
openssl_fips=openssl-fips-2.0.16
openssl_fips_tarball=${openssl_fips}.tar.gz
curl -LO https://openssl.org/source/${openssl_fips_tarball}
gzip -dc ${openssl_fips_tarball} | tar xf -
mv ${openssl_fips} ${node_version}/deps/openssl_fips

tar -zcf ${node_version}.tar.gz ${node_version}
rm -rf ${node_version}
