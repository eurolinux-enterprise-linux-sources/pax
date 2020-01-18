%global ALTERNATIVES            %{_sbindir}/alternatives

Summary: POSIX File System Archiver
Name: pax
Version: 3.4
Release: 17%{?dist}
License: BSD
Group: Applications/Archiving
Source: ftp://ftp.suse.com/pub/people/kukuk/pax/%{name}-%{version}.tar.bz2
URL:    ftp://ftp.suse.com/pub/people/kukuk/pax/
#use Linux PATH_MAX (4092) for maximum PATHLENGTH instead of pax default 3072
Patch0: pax-3.0-PATHMAX.patch
#fix bug with archiving files of filename length exactly 100 chars
Patch1: pax-3.4-abs100.patch
#do not truncate names when extracting
Patch2: pax-3.4-rdtruncate.patch
#do not fail with gcc-4.6+
Patch3: pax-gcc46.patch

# manpage edits - s/pax/opax/, add cross references
Patch4: pax-3.4-manpage.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires(post):  %{ALTERNATIVES}
Requires(preun): %{ALTERNATIVES}

%description
The 'pax' utility is the POSIX standard archive tool.  It supports the two most
common forms of standard Unix archive (backup) files - CPIO and TAR.

# "desired" alternative constants
%global ALT_NAME                pax
%global ALT_LINK                %{_bindir}/pax
%global ALT_SL1_NAME            pax-man
%global ALT_SL1_LINK            %{_mandir}/man1/pax.1.gz

# "local" alternative constants ("opax" - OpenBSD pax)
%global ALT_PATH                %{_bindir}/opax
%global ALT_SL1_PATH            %{_mandir}/man1/opax.1.gz

# helpers for alternatives
%global ALT_MAN_ORIG            %{_mandir}/man1/pax.1
%global ALT_MAN_NEW             %{_mandir}/man1/opax.1

%prep
%setup -q
%patch0 -p1 -b .PATHMAX
%patch1 -p1 -b .abs100
%patch2 -p1 -b .rdtruncate
%patch3 -p1 -b .gcc46
%patch4 -p1 -b .manpage

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
mv %{buildroot}%{ALT_LINK} %{buildroot}%{ALT_PATH}
mv %{buildroot}%{ALT_MAN_ORIG} %{buildroot}%{ALT_MAN_NEW}
ln -s %{ALT_PATH} %{buildroot}%{ALT_LINK}
ln -s %{ALT_MAN_NEW} %{buildroot}%{ALT_MAN_ORIG}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ABOUT-NLS AUTHORS ChangeLog COPYING NEWS README THANKS
%{ALT_PATH}
%doc %{ALT_SL1_PATH}
%ghost %verify(not md5 size mode mtime) %{ALT_LINK}
%ghost %verify(not md5 size mode mtime) %{ALT_SL1_LINK}

%post
# We need to remove old /usr/bin/pax binary because the following
# 'update-alternatives' step does not do it itself.  We may remove this once we
# are sure that pax >= 3.4-16 is installed on the system.
test -f %{ALT_LINK} && test ! -h %{ALT_LINK} && rm -rf %{ALT_LINK}

%{ALTERNATIVES} \
    --install   %{ALT_LINK}     %{ALT_NAME}     %{ALT_PATH}     33 \
    --slave     %{ALT_SL1_LINK} %{ALT_SL1_NAME} %{ALT_SL1_PATH} \

%preun
if [ $1 -eq 0 ]; then
    # only on pure uninstall (not upgrade)
    %{ALTERNATIVES} --remove %{ALT_NAME} %{ALT_PATH}
fi

%changelog
* Thu Jun 06 2013 Pavel Raiskup <praiskup@redhat.com> - 3.4-17
- remove old %%{_bindir}/pax binary if existent during update

* Wed May 15 2013 Pavel Raiskup <praiskup@redhat.com> - 3.4-16
- setup the 'alternatives' template (#929349)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Ondrej Vasik <ovasik@redhat.com> - 3.4-12
- fix FTBFS with gcc4.6+ - (#715754)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 19 2009 Ondrej Vasik <ovasik@redhat.com> - 3.4-8
- Merge review #226235: fix use of %%makeinstall as well

* Mon Jan 19 2009 Ondrej Vasik <ovasik@redhat.com> - 3.4-7
- Merge review #226235: do ship doc files,
  do comment patches, use better buildroot and
  defaults for attributes, allow parallel builds

* Fri Aug 29 2008 Ondrej Vasik <ovasik@redhat.com> - 3.4-6
- removed duplicate Source0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.4-5
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 3.4-4
- Rebuild for selinux ppc32 issue.

* Mon Jul 16 2007 Radek Brich <rbrich@redhat.com> - 3.4-3
- do not truncate file names when extracting (#205324)

* Wed Jun 20 2007 Radek Brich <rbrich@redhat.com> - 3.4-2
- applied patch for #239000 (pax fails creation of ustar
  if an absolute name is exactly 100 characters long)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.4-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.4-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.4-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Aug 15 2005 Peter Vrabec <pvrabec@redhat.com> 3.4-1
- upgrade 3.4

* Fri Mar 18 2005 Peter Vrabec <pvrabec@redhat.com> 3.0-11
- rebuilt

* Thu Oct 21 2004 Peter Vrabec <pvrabec@redhat.com>
- fix PAXPATHLEN (#132857)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 3.0-5
- rebuild on all arches

* Wed Jul 03 2002 Karsten Hopp <karsten@redhat.de>
- fix documentation (#63671)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Mar  5 2002 Matt Wilson <msw@redhat.com>
- pull PAX source tarball from the SuSE package (which is based off
  this one yet claims copyright on the spec file)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Fri Feb 23 2001 Jakub Jelinek <jakub@redhat.com>
- make it build under glibc 2.2.2

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun 30 2000 Preston Brown <pbrown@redhat.com>
- debian version, which is a port from OpenBSD's latest.

* Tue Jun 13 2000 Preston Brown <pbrown@redhat.com>
- FHS paths

* Tue May 30 2000 Preston Brown <pbrown@redhat.com>
- adopted for Winston.

