#!/bin/sh

export version=$(rpm -q --specfile --qf='%{version}\n' nodejs.spec | head -n1)
node_version=node-v${version}-rh

## Create the tarball
./create_node_tarball.sh
## Copy the tarball to SOURCES
mv ${node_version}.tar.gz /root/rpmbuild/SOURCES/${node_version}.tar.gz

if [ -d /root/.ccache ]; then
  CCACHE_HOME=/root/.ccache
  export CC='ccache gcc'
  export CXX='ccache g++'
  env
  ccache -s
fi

## Build the rpm
if [ "$SILENT" == "true" ]; then
  rpmbuild -ba --quiet --noclean --define='basebuild 0' --define='node_quiet 1' /root/rpmbuild/SPECS/nodejs.spec
else
  rpmbuild -ba --noclean --define='basebuild 0' --define='node_quiet 1' /root/rpmbuild/SPECS/nodejs.spec
fi
