#!/bin/sh

version=$(rpm -q --specfile --qf='%{version}\n' nodejs.spec | head -n1)
node_version=node-v${version}-rh

git clone https://github.com/bucharest-gold/node.git -b v${version}-rh ${node_version}
tar -zcf ${node_version}.tar.gz ${node_version}
rm -rf ${node_version}
