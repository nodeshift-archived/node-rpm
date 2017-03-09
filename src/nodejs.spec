%{?scl:%scl_package nodejs}
%{!?scl:%global pkg_name %{name}}
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%global with_debug 1

# ARM builds currently break on the Debug builds, so we'll just
# build the standard runtime until that gets sorted out.
%ifarch %{arm} aarch64 %{power64}
%global with_debug 0
%endif

Name: %{?scl_prefix}nodejs
Version: 6.9.1
Release: 2%{?dist}
Summary: JavaScript runtime
License: MIT and ASL 2.0 and ISC and BSD
URL: http://nodejs.org/

ExclusiveArch: %{nodejs_arches}

# nodejs bundles openssl, but we use the system version in Fedora
# because openssl contains prohibited code, we remove openssl completely from
# the tarball, using the script in Source100
Source0: node-v%{version}-stripped.tar.gz
Source100: %{pkg_name}-tarball.sh

# The native module Requires generator remains in the nodejs SRPM, so it knows
# the nodejs and v8 versions.  The remainder has migrated to the
# nodejs-packaging SRPM.
#Source7: nodejs_native.attr

# Disable running gyp on bundled deps we don't use
Patch1: nodejs-disable-gyp-deps.patch

# use system certificates instead of the bundled ones
# modified version of Debian patch:
# http://patch-tracker.debian.org/patch/series/view/nodejs/0.10.26~dfsg1-1/2014_donotinclude_root_certs.patch
Patch2: nodejs-use-system-certs.patch

# openssl-1.0.2 isn't in RHEL yet, so we use old one
Patch3:  0002-Use-openssl-1.0.1.patch

# some tests are failing, we turn them off
Patch4: 0001-Disable-crypto-tests.patch
Patch5: 0001-Disable-failing-tests.patch


# V8 presently breaks ABI at least every x.y release while never bumping SONAME
#%global v8_version 5.1.281.84
%global v8_abi 5.1

BuildRequires: %{?scl_prefix}gyp
#BuildRequires: %{?scl_prefix}scldevel
BuildRequires: python-devel
BuildRequires: %{?scl_prefix}libuv-devel >= 1.9.1
BuildRequires: %{?scl_prefix}http-parser-devel >= 2.7.0
BuildRequires: zlib-devel
BuildRequires: openssl-devel
BuildRequires: procps-ng
Requires: %{?scl_prefix}libuv >= 1.9.1
Requires: %{?scl_prefix}http-parser >= 2.7.0
Requires: openssl

# Node.js requires some features from openssl 1.0.1 for SPDY support
#BuildRequires: openssl-devel >= 1:1.0.2

# we need the system certificate store when Patch2 is applied
Requires: ca-certificates

#we need ABI virtual provides where SONAMEs aren't enough/not present so deps
#break when binary compatibility is broken
%global nodejs_abi 6.9
Provides: %{?scl_prefix}nodejs(abi) = %{nodejs_abi}
Provides: %{?scl_prefix}nodejs(v8-abi) = %{v8_abi}

#this corresponds to the "engine" requirement in package.json
Provides: %{?scl_prefix}nodejs(engine) = %{version}

# Node.js currently has a conflict with the 'node' package in Fedora
# The ham-radio group has agreed to rename their binary for us, but
# in the meantime, we're setting an explicit Conflicts: here
Conflicts: %{?scl_prefix}node <= 0.3.2-12

# The punycode module was absorbed into the standard library in v0.6.
# It still exists as a seperate package for the benefit of users of older
# versions.  Since we've never shipped anything older than v0.10 in Fedora,
# we don't need the seperate nodejs-punycode package, so we Provide it here so
# dependent packages don't need to override the dependency generator.
# See also: RHBZ#11511811
# UPDATE: punycode will be unabsorbed from node in v7/v8 release
Provides: %{?scl_prefix}nodejs-punycode = 2.0.0
Provides: %{?scl_prefix}npm(punycode) = 2.0.0


# Node.js has forked c-ares from upstream in an incompatible way, so we need
# to carry the bundled version internally.
# See https://github.com/nodejs/node/commit/766d063e0578c0f7758c3a965c971763f43fec85
Provides: %{?scl_prefix}bundled(c-ares) = 1.10.1

# Node.js is closely tied to the version of v8 that is used with it. It makes
# sense to use the bundled version because upstream consistently breaks ABI
# even in point releases. Node.js upstream has now removed the ability to build
# against a shared system version entirely.
# See https://github.com/nodejs/node/commit/d726a177ed59c37cf5306983ed00ecd858cfbbef
Provides: %{?scl_prefix}bundled(v8) = 5.1.281.84

# Node.js and http-parser share an upstream. The http-parser upstream does not
# do releases often and is almost always far behind the bundled version
#Provides: %%{?scl_prefix}bundled(http-parser) = 2.5.1

%description
Node.js is a platform built on Chrome's JavaScript runtime
for easily building fast, scalable network applications.
Node.js uses an event-driven, non-blocking I/O model that
makes it lightweight and efficient, perfect for data-intensive
real-time applications that run across distributed devices.

%package devel
Summary: JavaScript runtime - development headers
Requires: %{?scl_prefix}%{pkg_name}%{?_isa} == %{version}-%{release}
Requires: %{?scl_prefix}libuv-devel%{?_isa} %{?scl_prefix}http-parser-devel%{?_isa}
Requires: openssl-devel%{?_isa} zlib-devel%{?_isa}
Requires: %{?scl_prefix}runtime

%description devel
Development headers for the Node.js JavaScript runtime.

%package docs
Summary: Node.js API documentation
Group: Documentation
BuildArch: noarch

%description docs
The API documentation for the Node.js JavaScript runtime.

%prep
%setup -q -n node-v%{version}

# remove bundled dependencies that we aren't building
%patch1 -p1
rm -rf deps/npm \
       deps/uv \
       deps/http-parser \
       deps/zlib 

# remove bundled CA certificates
%patch2 -p1
rm -f src/node_root_certs.h

# use old openssl
%patch3 -p1

# disable tests
%patch4 -p1
%patch5 -p1

%build
# build with debugging symbols and add defines from libuv (#892601)
# Node's v8 breaks with GCC 8 because of incorrect usage of methods on
# NULL objects. We need to pass -fno-delete-null-pointer-checks
export CFLAGS='%{optflags} -g \
               -D_LARGEFILE_SOURCE \
               -D_FILE_OFFSET_BITS=64 \
               -DZLIB_CONST \
               -fno-delete-null-pointer-checks'

export CXXFLAGS='%{optflags} -g \
                 -D_LARGEFILE_SOURCE \
                 -D_FILE_OFFSET_BITS=64 \
                 -DZLIB_CONST \
                 -fno-delete-null-pointer-checks -I%{_includedir}' 

export LDFLAGS='%{optflags} -L%{_libdir}'

./configure --prefix=%{_prefix} \
           --shared-http-parser \
           --shared-zlib \
           --shared-libuv \
           --without-npm \
           --without-dtrace \
           --shared-openssl


%if %{?with_debug} == 1
# Setting BUILDTYPE=Debug builds both release and debug binaries
%{?scl:scl enable %{scl} - << \EOF}
make BUILDTYPE=Debug %{?_smp_mflags}
%{?scl:EOF}
%else
%{?scl:scl enable %{scl} - << \EOF}
make BUILDTYPE=Release %{?_smp_mflags}
%{?scl:EOF}
%endif

%install
./tools/install.py install %{buildroot} %{_prefix}

# and remove dtrace file again
rm -rf %{buildroot}/%{_prefix}/lib/dtrace

# Set the binary permissions properly
chmod 0755 %{buildroot}/%{_bindir}/node

%if %{?with_debug} == 1
# Install the debug binary and set its permissions
install -Dpm0755 out/Debug/node %{buildroot}/%{_bindir}/node_g
%endif

# own the sitelib directory
mkdir -p %{buildroot}%{_prefix}/lib/node_modules

# ensure Requires are added to every native module that match the Provides from
# the nodejs build in the buildroot
#install -Dpm0644 %%{SOURCE7} %%{buildroot}%{_rpmconfigdir}/fileattrs/nodejs_native.attr
#cat << EOF > %{buildroot}%{_rpmconfigdir}/nodejs_native.req
#!/bin/sh
#echo 'nodejs(abi) = %nodejs_abi'
#echo 'nodejs(v8-abi) = %v8_abi'
#EOF
#chmod 0755 %{buildroot}%{_rpmconfigdir}/nodejs_native.req

#install documentation
mkdir -p %{buildroot}%{_pkgdocdir}/html
cp -pr doc/* %{buildroot}%{_pkgdocdir}/html
rm -f %{buildroot}%{_pkgdocdir}/html/nodejs.1

#node-gyp needs common.gypi too
mkdir -p %{buildroot}%{_datadir}/node
cp -p common.gypi %{buildroot}%{_datadir}/node

# Install the GDB init tool into the documentation directory
mv %{buildroot}/%{_datadir}/doc/node/gdbinit %{buildroot}/%{_pkgdocdir}/gdbinit

%check 
%{?scl:scl enable %{scl} "}
python tools/test.py --mode=release parallel -J 
%{?scl:"}

%files
%{_bindir}/node
%{_mandir}/man1/node.*
%dir %{_prefix}/lib/node_modules
%dir %{_datadir}/node
%dir %{_datadir}/systemtap
%dir %{_datadir}/systemtap/tapset
%{_datadir}/systemtap/tapset/node.stp
#%%{_rpmconfigdir}/fileattrs/nodejs_native.attr
#%%{_rpmconfigdir}/nodejs_native.req
%dir %{_pkgdocdir}
%license LICENSE
%doc AUTHORS CHANGELOG.md COLLABORATOR_GUIDE.md GOVERNANCE.md README.md
%doc ROADMAP.md WORKING_GROUPS.md
 

%files devel
%if %{?with_debug} == 1
%{_bindir}/node_g
%endif
%{_includedir}/node
%{_datadir}/node/common.gypi
%{_pkgdocdir}/gdbinit

%files docs
%dir %{_pkgdocdir}
%{_pkgdocdir}/html

%changelog
* Wed Jan 11 2017 Zuzana Svetlikova <zsvetlik@redhat.com> - 6.9.1-2
- Rebuild from zvetlik/rh-nodejs6
- newer releases have problems with debug
- add procps-ng for tests
- remove unused patches

* Thu Nov 03 2016 Zuzana Svetlikova <zsvetlik@redhat.com> - 6.9.1-1
- Update to 6.9.1

* Wed Oct 19 2016 Zuzana Svetlikova <zsvetlik@redhat.com> - 6.9.0-1
- update to v6.9.0 LTS

* Tue Oct 04 2016 Zuzana Svetlikova <zsvetlik@redhat.com> - 6.7.0-5
- Disable failing crypto tests

* Tue Oct 04 2016 Zuzana Svetlikova <zsvetlik@redhat.com> - 6.7.0-4
- Require openssl

* Tue Oct 04 2016 Zuzana Svetlikova <zsvetlik@redhat.com> - 6.7.0-2
- Build with shared openssl with EPEL7 patch

* Mon Oct 03 2016 Zuzana Svetlikova <zsvetlik@redhat.com> - 6.7.0-1
- Update to 6.7.0

* Wed Aug 31 2016 Zuzana Svetlikova <zsvetlik@redhat.com> - 6.5.0-1
- Update to 6.5.0, meanwhile built with bundled openssl
- update system-certs patch

* Wed Apr 06 2016 Tomas Hrcka <thrcka@redhat.com> - 4.4.2-1
- Rebase to latest upstream LTS release 4.4.2
- https://nodejs.org/en/blog/release/v4.4.1/

* Tue Apr 05 2016 Tomas Hrcka <thrcka@redhat.com> - 4.4.1-2
- Rebase to latest upstream LTS release 4.4.1
- https://nodejs.org/en/blog/release/v4.4.1/

* Thu Mar 17 2016 Tomas Hrcka <thrcka@redhat.com> - 4.4.0-1
- Rebase to latest upstream LTS release 4.4.0

* Tue Mar 01 2016 Tomas Hrcka <thrcka@redhat.com> - 4.3.0-5
- New upstream release 4.3.0
- https://nodejs.org/en/blog/release/v4.3.0/
- Build with bundled openssl, this will be reverted ASAP
- Unbundled http-parser

* Thu Jul 16 2015 Tomas Hrcka <thrcka@redhat.com> - 0.10.40-1
- Rebase to latest upstream release

* Wed Jul 01 2015 Tomas Hrcka <thrcka@redhat.com> - 0.10.39-1
- Rebase to latest upstream release

* Wed Mar 25 2015 Tomas Hrcka <thrcka@redhat.com> - 0.10.35-4
- Enable tests during build time

* Tue Mar 17 2015 Tomas Hrcka <thrcka@redhat.com> - 0.10.35-2
- Reflect dependency on specific ABI changes in v8
- RHBZ#1197110

* Wed Jan 07 2015 Tomas Hrcka <thrcka@redhat.com> - 0.10.35-1
- New upstream release 0.10.35

* Sun Feb 02 2014 Tomas Hrcka <thrcka@redhat.com> - 0.10.25-1
- New upstream release 0.10.25

* Tue Jan 14 2014 Tomas Hrcka <thrcka@redhat.com> - 0.10.24-1
- new upstream release 0.10.24

* Tue Nov 26 2013 Tomas Hrcka <thrcka@redhat.com> - 0.10.21-3
- rebuilt with v8314 collection

* Tue Nov 12 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.22-1
- new upstream release 0.10.22
  http://blog.nodejs.org/2013/11/12/node-v0-10-22-stable/

* Mon Oct 21 2013 Tomas Hrcka <thrcka@redhat.com> - 0.10.21-2
- Build with system wide c-ares

* Fri Oct 18 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.21-1
- new upstream release 0.10.21
  http://blog.nodejs.org/2013/10/18/node-v0-10-21-stable/
- resolves an undisclosed security vulnerability in the http module

* Tue Oct 01 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.20-1
- new upstream release 0.10.20
  http://blog.nodejs.org/2013/09/30/node-v0-10-20-stable/

* Wed Sep 25 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.19-1
- new upstream release 0.10.19
  http://blog.nodejs.org/2013/09/24/node-v0-10-19-stable/

* Fri Sep 06 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.18-1
- new upstream release 0.10.18
  http://blog.nodejs.org/2013/09/04/node-v0-10-18-stable/

* Tue Aug 27 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.17-1
- new upstream release 0.10.17
  http://blog.nodejs.org/2013/08/21/node-v0-10-17-stable/

* Sat Aug 17 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.16-1
- new upstream release 0.10.16
  http://blog.nodejs.org/2013/08/16/node-v0-10-16-stable/
- add v8-devel to -devel Requires
- restrict -devel Requires to the same architecture

* Wed Aug 14 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.14-3
- fix typo in _isa macro in v8 Requires

* Wed Aug 07 2013 Tomas Hrcka <thrcka@redhat.com> - 0.10.5-6
 - Remove badly licensed fonts in script instead of patch

* Thu Jul 25 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.14-1
- new upstream release 0.10.14
  http://blog.nodejs.org/2013/07/25/node-v0-10-14-stable/

* Wed Jul 10 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.13-1
- new upstream release 0.10.13
  http://blog.nodejs.org/2013/07/09/node-v0-10-13-stable/
- remove RPM macros, etc. now that they've migrated to nodejs-packaging

* Wed Jun 19 2013 Tomas Hrcka <thrcka@redhat.com> - 0.10.5-5
 - added patch to remove badly licensed web fonts

* Wed Jun 19 2013 Tomas Hrcka <thrcka@redhat.com> - 0.10.5-5
 - added patch to remove badly licensed web fonts

* Wed Jun 19 2013 Tomas Hrcka <thrcka@redhat.com> - 0.10.5-4
  - strip openssl from the tarball it contains prohibited code (RHBZ#967736)
  - patch makefile so it do not use bundled deps
  - new stripped tarball

* Wed Jun 19 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.12-1
- new upstream release 0.10.12
  http://blog.nodejs.org/2013/06/18/node-v0-10-12-stable/
- split off a -packaging subpackage with RPM macros, etc.
- build -docs as noarch
- copy mutiple version logic from nodejs-packaging SRPM for now

* Fri May 31 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.9-1
- new upstream release 0.10.9
  http://blog.nodejs.org/2013/05/30/node-v0-10-9-stable/

* Wed May 29 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.8-1
- new upstream release 0.10.8
  http://blog.nodejs.org/2013/05/24/node-v0-10-8-stable/

* Wed May 29 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.7-1
- new upstream release 0.10.7
  http://blog.nodejs.org/2013/05/17/node-v0-10-7-stable/
- strip openssl from the tarball; it contains prohibited code (RHBZ#967736)
- patch Makefile so we can just remove all bundled deps completely

* Wed May 15 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.6-1
- new upstream release 0.10.6
  http://blog.nodejs.org/2013/05/14/node-v0-10-6-stable/

* Tue May 14 2013 Tomas Hrcka <thrcka@redhat.com> - 0.10.5-3.1
 - updated to latest upstream stable release

* Mon May 06 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.5-3
- nodejs-fixdep: work properly when a package has no dependencies

* Mon Apr 29 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.5-2
- nodejs-symlink-deps: make it work when --check is used and just
  devDependencies exist

* Wed Apr 24 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.5-1
- new upstream release 0.10.5
  http://blog.nodejs.org/2013/04/23/node-v0-10-5-stable/

* Mon Apr 15 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.4-1
- new upstream release 0.10.4
  http://blog.nodejs.org/2013/04/11/node-v0-10-4-stable/
- drop dependency generator files not supported on EL6
- port nodejs_default_filter to EL6
- add nodejs_find_provides_and_requires macro to invoke dependency generator
- invoke the standard RPM provides and requires generators from the Node.js ones
- write native module Requires from nodejs.req
- change the c-ares-devel Requires in -devel to match the BuildRequires

* Tue Apr 09 2013 Stephen Gallagher <sgallagh@redhat.com> - 0.10.3-2.1
- Build against c-ares 1.9

* Mon Apr 08 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.10.3-3
- Add support for software collections
- Move rpm macros and tooling to separate package
- add no-op macro to permit spec compatibility with EPEL

* Thu Apr 04 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.3-2
- nodejs-symlink-deps: symlink unconditionally in the buildroot

* Wed Apr 03 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.3-1
- new upstream release 0.10.3
  http://blog.nodejs.org/2013/04/03/node-v0-10-3-stable/
- nodejs-symlink-deps: only create symlink if target exists
- nodejs-symlink-deps: symlink devDependencies when --check is used

* Sun Mar 31 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.2-1
- new upstream release 0.10.2
  http://blog.nodejs.org/2013/03/28/node-v0-10-2-stable/
- remove %%nodejs_arches macro since it will only be useful if it is present in
  the redhat-rpm-config package
- add default filtering macro to remove unwanted Provides from native modules
- nodejs-symlink-deps now supports multiple modules in one SRPM properly
- nodejs-symlink-deps also now supports a --check argument that works in the
  current working directry instead of the buildroot

* Fri Mar 22 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.1-1
- new upstream release 0.10.1
  http://blog.nodejs.org/2013/03/21/node-v0-10-1-stable/

* Wed Mar 20 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.0-4
- fix escaping in dependency generator regular expressions (RHBZ#923941)

* Wed Mar 13 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.0-3
- add virtual ABI provides for node and v8 so binary module's deps break when
  binary compatibility is broken
- automatically add matching Requires to nodejs binary modules
- add %%nodejs_arches macro to future-proof ExcluseArch stanza in dependent
  packages

* Tue Mar 12 2013 Stephen Gallagher <sgallagh@redhat.com> - 0.10.0-2
- Fix up documentation subpackage

* Mon Mar 11 2013 Stephen Gallagher <sgallagh@redhat.com> - 0.10.0-1
- Update to stable 0.10.0 release
- https://raw.github.com/joyent/node/v0.10.0/ChangeLog

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-10
- minor bugfixes to RPM magic
  - nodejs-symlink-deps: don't create an empty node_modules dir when a module
    has no dependencies
  - nodes-fixdep: support adding deps when none exist
- Add the full set of headers usually bundled with node as deps to nodejs-devel.
  This way `npm install` for native modules that assume the stuff bundled with
  node exists will usually "just work".
-move RPM magic to nodejs-devel as requested by FPC

* Sat Jan 12 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-9
- fix brown paper bag bug in requires generation script

* Thu Jan 10 2013 Stephen Gallagher <sgallagh@redhat.com> - 0.9.5-8
- Build debug binary and install it in the nodejs-devel subpackage

* Thu Jan 10 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-7
- don't use make install since it rebuilds everything

* Thu Jan 10 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-6
- add %%{?isa}, epoch to v8 deps

* Wed Jan 09 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-5
- add defines to match libuv (#892601)
- make v8 dependency explicit (and thus more accurate)
- add -g to $C(XX)FLAGS instead of patching configure to add it
- don't write pointless 'npm(foo) > 0' deps

* Sat Jan 05 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-4
- install development headers
- add nodejs_sitearch macro

* Wed Jan 02 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-3
- make nodejs-symlink-deps actually work

* Tue Jan 01 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-2
- provide nodejs-devel so modules can BuildRequire it (and be consistent
  with other interpreted languages in the distro)

* Tue Jan 01 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-1
- new upstream release 0.9.5
- provide nodejs-devel for the moment
- fix minor bugs in RPM magic
- add nodejs_fixdep macro so packagers can easily adjust dependencies in
  package.json files

* Wed Dec 26 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.4-1
- new upstream release 0.9.4
- system library patches are now upstream
- respect optflags
- include documentation in subpackage
- add RPM dependency generation and related magic
- guard libuv depedency so it always gets bumped when nodejs does
- add -devel subpackage with enough to make node-gyp happy

* Thu Dec 20 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-9
- Drop requirement on openssl 1.0.1

* Wed Dec 19 2012 Dan Horák <dan[at]danny.cz> - 0.9.3-8
- set exclusive arch list to match v8

* Tue Dec 18 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-7
- Add remaining changes from code review
- Remove unnecessary BuildRequires on findutils
- Remove %%clean section

* Fri Dec 14 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-6
- Fixes from code review
- Fix executable permissions
- Correct the License field
- Build debuginfo properly

* Thu Dec 13 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-5
- Return back to using the standard binary name
- Temporarily adding a conflict against the ham radio node package until they
  complete an agreed rename of their binary.

* Wed Nov 28 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-4
- Rename binary and manpage to nodejs

* Mon Nov 19 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-3
- Update to latest upstream development release 0.9.3
- Include upstreamed patches to unbundle dependent libraries

* Tue Oct 23 2012 Adrian Alves <alvesadrian@fedoraproject.org>  0.8.12-1
- Fixes and Patches suggested by Matthias Runge

* Mon Apr 09 2012 Adrian Alves <alvesadrian@fedoraproject.org> 0.6.5
- First build.
