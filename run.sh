#!/bin/sh

export version=$(rpm -q --specfile --qf='%{version}\n' nodejs.spec | head -n1)
node_version=node-v${version}-rh

pushd /opt/app-root/src/rpmbuild/BUILD/node
git fetch --tags
git checkout v${version}-rh
cd ..
ln -s node rhoar-nodejs-${version}
popd

## Build the rpm
if [ $SILENT == "true" ]; then
  rpmbuild -ba --quiet --noclean --define='basebuild 0' /opt/app-root/src/rpmbuild/SPECS/nodejs.spec
else
  rpmbuild -ba --noclean --define='basebuild 0' /opt/app-root/src/rpmbuild/SPECS/nodejs.spec
fi
