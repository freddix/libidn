Summary:	Internationalized string processing library
Name:		idn
Version:	1.28
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://ftp.gnu.org/gnu/libidn/libidn-%{version}.tar.gz
# Source0-md5:	43a6f14b16559e10a492acc65c4b0acc
Patch0:		libidn-python.patch
URL:		http://www.gnu.org/software/libidn/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libtool
BuildRequires:	perl-base
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	texinfo
Requires:	libidn = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU Libidn is an implementation of the Stringprep, Punycode and IDNA
specifications defined by the IETF Internationalized Domain Names
(IDN) working group, used for internationalized domain names.

%package -n libidn
Summary:	Header files for libidn library
Group:		Libraries

%description -n libidn
libidn library.

%package -n libidn-devel
Summary:	Header files for libidn library
Group:		Development/Libraries
Requires:	libidn = %{version}-%{release}

%description -n libidn-devel
Header files for libidn library.

%package -n python-idn
Summary:	Python interface to libidn
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-idn
Python interface to libidn (internationalized domain names library).

%prep
%setup -qn libidn-%{version}
%patch0 -p1

# don't fail on AM warnings
%{__sed} -i -e '/AM_INIT_AUTOMAKE/s/-Werror//' configure.ac

%build
%{__libtoolize}
%{__aclocal} -I m4 -I gl/m4 -I lib/gl/m4
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	--disable-static
%{__make}

%{__make} -C contrib/idn-python \
	INCLUDE="%{py_incdir} %{rpmcflags} -I../../lib -L../../lib/.libs"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D contrib/idn-python/idn.so $RPM_BUILD_ROOT%{py_sitedir}/idn.so

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -rf $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp

%find_lang libidn

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%post	-n libidn -p /sbin/ldconfig
%postun	-n libidn -p /sbin/ldconfig

%files -f libidn.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FAQ NEWS README* THANKS TODO doc/libidn.html contrib
%attr(755,root,root) %{_bindir}/idn
%{_mandir}/man1/idn.1*
%{_infodir}/libidn.info*

%files -n libidn
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libidn.so.??
%attr(755,root,root) %{_libdir}/libidn.so.*.*.*

%files -n libidn-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libidn.so
%{_libdir}/libidn.la
%{_includedir}/*.h
%{_pkgconfigdir}/libidn.pc
%{_mandir}/man3/*

%files -n python-idn
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/idn.so

