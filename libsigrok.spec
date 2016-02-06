Name:           libsigrok
Version:        0.4.0
Release:        0%{?dist}
Summary:        Basic hardware access drivers for logic analyzers
# Combined GPLv3+ and GPLv2+ and BSD
License:        GPLv3+
URL:            http://www.sigrok.org/
Source0:        http://sigrok.org/download/source/libsigrok/%{name}-%{version}.tar.gz

BuildRequires:  glib2-devel
BuildRequires:  glibmm24-devel
BuildRequires:  libzip-devel
BuildRequires:  zlib-devel
BuildRequires:  libieee1284-devel
BuildRequires:  libusb1-devel
BuildRequires:  libftdi-devel
BuildRequires:  libserialport-devel     >= 0.1.1
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  libtool

%description
%{name} is a shared library written in C which provides the basic API
for talking to hardware and reading/writing the acquired data into various
input/output file formats.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        cxx
Summary:        C++ bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    cxx
The %{name}-cxx package contains C++ libraries for %{name}.

%package        cxx-devel
Summary:        Development files for  %{name} C++ bindings
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    cxx-devel
The %{name}-cxx-devel package contains libraries and header files for
developing applications that use %{name} C++ bindings.

%package        doc
Group:          Documentation
Summary:        API documentation for %{name}
BuildArch:      noarch

%description    doc
The %{name}-doc package contains documentation for developing software
with %{name}.


%prep
%setup -q
# Replace GROUP="plugdev" with TAG+="uaccess"
sed 's/MODE=\"[0-9]*\", GROUP=\"plugdev\"/TAG += \"uaccess\"/g' contrib/z60_libsigrok.rules -i


%build
%configure --disable-static
make %{?_smp_mflags} V=1

# This builds documentation for the -doc package
doxygen Doxyfile


%install
%make_install
# Install udev rules
install -D -p -m 0644 contrib/z60_libsigrok.rules %{buildroot}%{_udevrulesdir}/60-libsigrok.rules

find %{buildroot} -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc README README.devices NEWS COPYING
%{_libdir}/libsigrok.so.3*
%{_udevrulesdir}/60-libsigrok.rules

%files devel
%{_includedir}/libsigrok/
%{_libdir}/libsigrok.so
%{_libdir}/pkgconfig/libsigrok.pc

%files cxx
%{_libdir}/libsigrokcxx.so.3*

%files cxx-devel
%{_includedir}/libsigrokcxx/
%{_libdir}/libsigrokcxx.so
%{_libdir}/pkgconfig/libsigrokcxx.pc

%files doc
%doc doxy/html-api/


%changelog
* Sat Feb 06 2016 Alexandru Gagniuc <mr.nuke.me@gmail.com> - 0.4.0-0
- Update to libsigrok 0.4.0
- Convert GROUP="plugdev" udev rules to TAG+="uaccess" using sed
- Add "cxx" and "cxx-devel" packages for C++ bindings.
- Add minimum version (0.1.1) for libserialport-devel package
- Add libieee1284-devel dependency for "hung-chang-dso-2100" driver
- Remove autoreconf step, as it is no longer needed

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 04 2016 Alexandru Gagniuc <mr.nuke.me@gmail.com> - 0.3.0-4
- Fix used rules to use "uaccess" tag instead of "plugdev" group

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 06 2015 Remi Collet <remi@fedoraproject.org> - 0.3.0-2
- rebuild for new libzip

* Sat Sep 20 2014 Dan Horák <dan[at]danny.cz> - 0.3.0-1
- update to libsigrok 0.3.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 10 2014 Dan Horák <dan[at]danny.cz> - 0.2.2-3
- rebuilt for libftdi1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 04 2013 Dan Horák <dan[at]danny.cz> - 0.2.2-1
- update to libsigrok 0.2.2

* Mon Nov 04 2013 Dan Horák <dan[at]danny.cz> - 0.2.1-4
- udev rules should react also on the usbmisc subsystem

* Sun Nov 03 2013 Dan Horák <dan[at]danny.cz> - 0.2.1-3
- scan /sys/class/usbmisc
- add support for Rigol DS1152 scopes with upgraded bandwidth
- resolves: #1025968

* Wed Aug 21 2013 Remi Collet <rcollet@redhat.com> - 0.2.1-2
- rebuild for new libzip

* Fri Aug 09 2013 Alexandru Gagniuc <mr.nuke.me@gmail.com> - 0.2.1-1
- Update to libsigrok 0.2.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 04 2013 Alexandru Gagniuc <mr.nuke.me@gmail.com> - 0.2.0-1
- Update to libsigrok 0.2.0 (inlcudes soname version bump)
- All working drivers are enabled by default. Don't manually enable them.
- Package provided udev rules
- Remove unneeded 'rm -rf buildroot'
- Remove unneeded 'defattr'
- Remove ChangeLog from documentation (only contains a git log)

* Wed Mar 13 2013 Alexandru Gagniuc <mr.nuke.me@gmail.com> - 0.1.1-3
- Drop dependency of -doc subpackage
- Use explicit soversion in files section

* Sat Dec 01 2012 Alexandru Gagniuc <mr.nuke.me@gmail.com> - 0.1.1-2
- Add comment explaining chioce of license
- Removed  _missing_build_ids_terminate_build undef
- Add comment explaining doxygen warnings

* Wed Oct 10 2012 Alexandru Gagniuc mr.nuke.me[at]gmail[dot]com - 0.1.1-1
- Initial RPM release
