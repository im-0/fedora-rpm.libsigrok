Name:           libsigrok
Version:        0.2.1
Release:        2%{?dist}
Summary:        Basic hardware access drivers for logic analyzers
# Combined GPLv3+ and GPLv2+ and BSD
License:        GPLv3+
URL:            http://www.sigrok.org/
Source0:        http://sigrok.org/download/source/libsigrok/%{name}-%{version}.tar.gz

BuildRequires:  glib2-devel
BuildRequires:  libzip-devel
BuildRequires:  zlib-devel
BuildRequires:  libusb1-devel
BuildRequires:  libftdi-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  doxygen
BuildRequires:  graphviz
# link-mso19 driver was disabed by upstream for this release (only udev user)
#BuildRequires:  libudev-devel

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


%package        doc
Group:          Documentation
Summary:        API documentation for %{name}
BuildArch:      noarch

%description    doc
The %{name}-doc package contains documentation for developing software
with %{name}.

%prep
%setup -q


%build
# alsa is the only driver that gets autodisabled when alsa-lib-devel is not
# found, so we explicitly enable it to be sure we compile it
%configure --disable-static --enable-alsa
make %{?_smp_mflags}

# This builds documentation for the -doc package
doxygen Doxyfile


%install
%make_install
# Install udev rules
install -D -p -m 0644 contrib/z60_libsigrok.rules %{buildroot}/lib/udev/rules.d/60_libsigrok.rules


find %{buildroot} -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc README README.devices NEWS COPYING
%{_libdir}/libsigrok.so.1*
/lib/udev/rules.d/60_libsigrok.rules

%files devel
%{_includedir}/libsigrok/
%{_libdir}/libsigrok.so
%{_libdir}/pkgconfig/libsigrok.pc

%files doc
%doc doxy/html-api/

%changelog
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
