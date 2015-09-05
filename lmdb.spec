#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Memory-mapped key-value database
Name:		lmdb
Version:	0.9.16
Release:	1
License:	OpenLDAP
Group:		Libraries
Source0:	https://github.com/LMDB/lmdb/archive/LMDB_%{version}.tar.gz
# Source0-md5:	0de89730b8f3f5711c2b3a4ba517b648
URL:		http://symas.com/mdb/
Patch0:		%{name}-make.patch
BuildRequires:	doxygen
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LMDB is an ultra-fast, ultra-compact key-value embedded data store
developed by for the OpenLDAP Project. By using memory-mapped files,
it provides the read performance of a pure in-memory database while
still offering the persistence of standard disk-based databases, and
is only limited to the size of the virtual address space.

%package libs
Summary:	Shared libraries for %{name}
Group:		Libraries

%description libs
The %{name}-libs package contains shared libraries necessary for
running applications that use %{name}.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}-LMDB_%{version}
%patch0 -p1

%build
cd libraries/liblmdb
%{__make} \
	CC="%{__cc}" \
	XCFLAGS="%{rpmcflags} %{rpmcppflags}"

%if %{with tests}
rm -rf testdb
LD_LIBRARY_PATH=$PWD %{__make} test
%endif

# Build doxygen documentation
doxygen
# remove unpackaged files
rm -f Doxyfile
rm -rf man # Doxygen generated manpages
cd ../../

%install
rm -rf $RPM_BUILD_ROOT

# make install expects existing directory tree
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir}/man1}

%{__make} -C libraries/liblmdb install \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix} \
	libprefix=%{_libdir} \
	manprefix=%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mdb_copy
%attr(755,root,root) %{_bindir}/mdb_dump
%attr(755,root,root) %{_bindir}/mdb_load
%attr(755,root,root) %{_bindir}/mdb_stat
%{_mandir}/man1/mdb_copy.1*
%{_mandir}/man1/mdb_dump.1*
%{_mandir}/man1/mdb_load.1*
%{_mandir}/man1/mdb_stat.1*

%files libs
%defattr(644,root,root,755)
%doc libraries/lib%{name}/CHANGES
%attr(755,root,root) %{_libdir}/liblmdb.so.0*

%files devel
%defattr(644,root,root,755)
%{_includedir}/lmdb.h
%attr(755,root,root) %{_libdir}/liblmdb.so
