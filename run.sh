#!/bin/sh

export version=$(rpm -q --specfile --qf='%{version}\n' nodejs.spec | head -n1)
node_version=node-v${version}-rh

## Create the tarball
./create_node_tarball.sh
## Copy the tarball to SOURCES
mv ${node_version}.tar.gz ${RPMBUILD_DIR}/SOURCES/${node_version}.tar.gz

## Build the rpm
rpmbuild -ba --noclean --define='basebuild 0' ${RPMBUILD_DIR}/SPECS/nodejs.spec
