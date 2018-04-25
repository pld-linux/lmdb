#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Memory-mapped key-value database
Summary(pl.UTF-8):	Baza danych klucz-wartość odwzorowywana w pamięci
Name:		lmdb
Version:	0.9.22
Release:	1
License:	OpenLDAP
Group:		Applications/Databases
#Source0Download: https://github.com/LMDB/lmdb/releases
Source0:	https://github.com/LMDB/lmdb/archive/LMDB_%{version}.tar.gz
# Source0-md5:	64c6132f481281b7b2ad746ecbfb8423
Patch0:		%{name}-make.patch
URL:		http://symas.com/mdb/
BuildRequires:	doxygen
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LMDB is an ultra-fast, ultra-compact key-value embedded data store
developed by for the OpenLDAP Project. By using memory-mapped files,
it provides the read performance of a pure in-memory database while
still offering the persistence of standard disk-based databases, and
is only limited to the size of the virtual address space.

%description -l pl.UTF-8
LMDB to bardzo szybka i zwarta, wbudowana baza danych klucz-wartość
rozwijana dla projektu OpenLDAP. Dzięki użyciu plików odwzorowywanych
w pamięci zapewnia wydajność odczytu analogiczną do bazydanych
trzymanej w pamięci, oferując jednocześnie trwałość charakterystyczną
dla baz opartych na dysku oraz ograniczenie wyłącznie rozmiarem
wirtualnej przestrzeni adresowej.

%package libs
Summary:	LMDB shared library
Summary(pl.UTF-8):	Biblioteka współdzielona LMDB
Group:		Libraries

%description libs
This package contains the shared library necessary for running
applications that use LMDB.

%description libs -l pl.UTF-8
Ten pakiet zawiera bibliotekę współdzieloną konieczną do uruchamiania
aplikacji wykorzystujących LMDB.

%package devel
Summary:	Header files for LMDB library
Summary(pl.UTF-8):	Plik nagłówkowy LMDB
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the header file for developing applications that
use LMDB.

%description devel -l pl.UTF-8
Ten pakiet zawiera plik nagłówkowy do tworzenia aplikacji
wykorzystujących LMDB.

%package static
Summary:	Static LMDB library
Summary(pl.UTF-8):	Statyczna biblioteka LMDB
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LMDB library.

%description static -l pl.UTF-8
Statyczna biblioteka LMDB.

%package apidocs
Summary:	LMDB API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki LMDB
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
LMDB API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki LMDB.

%prep
%setup -q -n %{name}-LMDB_%{version}
%patch0 -p1

%{__mv} libraries/liblmdb/* .

%build
%{__make} \
	CC="%{__cc}" \
	XCFLAGS="%{rpmcflags} %{rpmcppflags}"

%if %{with tests}
rm -rf testdb
LD_LIBRARY_PATH=$PWD %{__make} test
%endif

# Build doxygen documentation
doxygen

%install
rm -rf $RPM_BUILD_ROOT

# make install expects existing directory tree
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir}/man1}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix} \
	libdir=%{_libdir}

# rename to have typical 0.0.0 file
ln -sf liblmdb.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/liblmdb.so
%{__mv} $RPM_BUILD_ROOT%{_libdir}/liblmdb.so.{0,0.0.0}
/sbin/ldconfig -n  $RPM_BUILD_ROOT%{_libdir}

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
%doc CHANGES COPYRIGHT LICENSE
%attr(755,root,root) %{_libdir}/liblmdb.so.*.*.*
%ghost %{_libdir}/liblmdb.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblmdb.so
%{_includedir}/lmdb.h

%files static
%defattr(644,root,root,755)
%{_libdir}/liblmdb.a

%files apidocs
%defattr(644,root,root,755)
%doc html/*
