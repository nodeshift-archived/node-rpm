#!/bin/sh

version=$(rpm -q --specfile --qf='%{version}\n' nodejs.spec | head -n1)
echo "Building with version $version"

old_build_dir=$(ls -d /root/rpmbuild_usr_src_debug/BUILD/node-v*)
new_build_dir=$(dirname $old_build_dir)/node-v${version}
echo "old_build_dir:" ${old_build_dir}
echo "new_build_dir:" ${new_build_dir}

ln -s $old_build_dir $new_build_dir

pushd ${new_build_dir}
git fetch origin refs/tags/v${version}:refs/tags/v${version}
## remove addons before checking out
rm -rf test/addons
rm -rf test/addons-napi
git checkout -fb ${version} v${version}
popd

pushd $(dirname $new_build_dir)
rpmbuild -bc --noclean --define='basebuild 1' /usr/src/node-rpm/nodejs.spec
popd

unlink $new_build_dir
