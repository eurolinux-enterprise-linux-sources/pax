#
# spec file for package pax (Version 3.2)
#
# Copyright (c) 2003 SuSE Linux AG, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://www.suse.de/feedback/
#

# norootforbuild
# neededforbuild  
# usedforbuild    aaa_base acl attr bash bind9-utils bison cpio cpp cvs cyrus-sasl cyrus-sasl2 db devs diffutils e2fsprogs file filesystem fileutils fillup findutils flex gawk gdbm-devel glibc glibc-devel glibc-locale gpm grep groff gzip insserv kbd less libacl libattr libgcc libstdc++ libxcrypt m4 make man mktemp modutils ncurses ncurses-devel net-tools netcfg pam pam-devel pam-modules patch permissions ps rcs readline sed sendmail sh-utils shadow strace syslogd sysvinit tar texinfo textutils timezone unzip util-linux vim zlib-devel autoconf automake binutils bzip2 cracklib gcc gdbm gettext libtool perl rpm zlib

Name:         pax
Summary:      POSIX File System Archiver
Version:      3.3
Release:      0
License:      BSD
Autoreqprov:  on
Prefix:       %{_prefix}
Group:        Productivity/Archiving/Backup
Source:       %{name}-%{version}.tar.bz2
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
pax is the POSIX standard archive tool.  It supports the two most
common forms of standard archive (backup) files - CPIO and TAR.

%prep
%setup -q

%build
export CFLAGS=$RPM_OPT_FLAGS
./configure --prefix=%{_prefix} --mandir=%{_mandir} %{_target_cpu}-suse-linux
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/pax
%doc %{_mandir}/man1/*

%changelog
* Fri Jul 29 2005 - kukuk@suse.de
- Update to pax 3.3 (LFS support, -O option)
* Fri Oct 17 2003 - kukuk@suse.de
- Update to pax 3.2 (sync with OpenBSD version, fix compiler
  warnings).
* Fri Jan 17 2003 - kukuk@suse.de
- Update to pax 3.1 (sync with OpenBSD version, fix compiler
  warnings).
* Tue Jan 01 2002 - kukuk@suse.de
- New version, passes now all LSB tests
* Fri Dec 14 2001 - kukuk@suse.de
- Initial version
