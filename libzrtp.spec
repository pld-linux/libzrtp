#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	sqlite3		# SQLite based cache
%bcond_without	tests		# do not perform "make check"

%define	snap	20120707
%define	rel	3

Summary:	Phil Zimmermann's SDK for ZRTP
Summary(pl.UTF-8):	SDK ZRTP Phila Zimmermanna
Name:		libzrtp
Version:	1.2.0
Release:	0.%{snap}.%{rel}
License:	AGPL v3 with FreeSWITCH exception or commercial
Group:		Libraries
Source0:	https://github.com/traviscross/libzrtp/archive/master.tar.gz
# Source0-md5:	58bddacc5a35f3271c7c7095e8b35d49
Patch0:		%{name}-shared.patch
Patch1:		features.patch
URL:		http://zfoneproject.com/prod_sdk.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bnlib-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libtool
%{?with_sqlite3:BuildRequires:	sqlite3-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libZRTP SDK library implements the ZRTP secure VoIP protocol.

%description -l pl.UTF-8
Biblioteka libZRTP SDK implementuje bezpieczny protokół VoIP ZRTP.

%package devel
Summary:	Header files for ZRTP library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ZRTP
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	bnlib-devel
%{?with_sqlite3:Requires:	sqlite3-devel}

%description devel
Header files for ZRTP library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ZRTP.

%package static
Summary:	Static ZRTP library
Summary(pl.UTF-8):	Statyczna biblioteka ZRTP
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ZRTP library.

%description static -l pl.UTF-8
Statyczna biblioteka ZRTP.

%package apidocs
Summary:	ZRTP API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki ZRTP
Group:		Documentation

%description apidocs
API documentation for ZRTP library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki ZRTP.

%prep
%setup -q -n %{name}-master
%patch -P0 -p1
%patch -P1 -p1

head -n78 src/zrtp_legal.c >LEGAL

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_sqlite3:--with-sqlite}
%{__make}

%{?with_apidocs:%{__make} doc}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_mandir}/man3
cp -p doc/out/man/man3/zrtp*.3 $RPM_BUILD_ROOT%{_mandir}/man3
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog LEGAL README
%attr(755,root,root) %{_libdir}/libzrtp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzrtp.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzrtp.so
%{_libdir}/libzrtp.la
%{_includedir}/libzrtp
%{?with_apidocs:%{_mandir}/man3/zrtp*.3*}

%files static
%defattr(644,root,root,755)
%{_libdir}/libzrtp.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/out/html/*
%endif
