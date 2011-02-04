%define tkver	8.4
#
Summary:	Tile - an improved themeing engine for Tk
Summary(pl.UTF-8):	Tile - ulepszony silnik motywów dla Tk
Name:		tile
Version:	0.7.8
Release:	1
License:	BSD
Group:		Development/Languages/Tcl
Source0:	http://dl.sourceforge.net/tktable/%{name}-%{version}.tar.gz
# Source0-md5:	1172c1875ae63d7a73d8ba27835e16d4
Patch0:		%{name}-pkg_lib_file.patch
URL:		http://tktable.sourceforge.net/tile/
BuildRequires:	autoconf
BuildRequires:	tk-devel >= %{tkver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_ulibdir	/usr/lib

%description
The Tile Widget Set is a next-generation re-implementation of many of
the core Tk widgets, along with the addition of several new widgets.
With Tile, Tk applications can achieve an appearance much closer to
native platform widgets, as well as take advantage of a modern, highly
dynamic theme engine to produce a wide variety of alternative user
interface styles. Tile widgets complement the existing Tk widgets, and
Tile is currently being incorporated directly into Tk.

%description -l pl.UTF-8
Zestaw Widgetów Tile jest nowej generacji reimplementacją wielu z
podstawowych widgetów Tk oraz rozszerzeniem ich o kilka nowych. Przy
użyciu Tile aplikacje Tk mogą zyskać nowy wygląd, znacznie bliższy
natywnemu dla danej platformy, a także wykorzystać nowoczesny,
dynamiczny silnik obsługi motywów do wytworzenia różnorodnych,
alternatywnych stylów użytkownika. Zestaw widgetów Tile uzupełnia
istniejące elementy Tk i jest obecnie do niego wcielany.

%package devel
Summary:	Tile - development files
Summary(pl.UTF-8):	Tile - pliki rozwojowe
Group:		Development/Languages/Tcl
Requires:	%{name} = %{version}-%{release}
Requires:	tk-devel >= %{tkver}

%description devel
The Tile Widget Set development files.

%description devel -l pl.UTF-8
Pliki rozwojowe Zestawu Widgetów Tile.

%package demo
Summary:	Tile - demo programs
Summary(pl.UTF-8):	Tile - programy demonstracyjne
Group:		Development/Languages/Tcl
Requires:	%{name} = %{version}-%{release}

%description demo
The Tile Widget Set demo programs.

%description demo -l pl.UTF-8
Programy demonstracyjne Zestawu Widgetów Tile.

%prep
%setup -q
%patch0 -p1

%build
%{__autoconf}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir},%{_ulibdir}}

%{__make} install \
	 DESTDIR=$RPM_BUILD_ROOT

if [ "%{_libdir}" != "%{_ulibdir}" ] ; then
	mv $RPM_BUILD_ROOT%{_libdir}/%{name}%{version} $RPM_BUILD_ROOT%{_ulibdir}
	ln -sf %{_libdir}/lib%{name}%{version}.so $RPM_BUILD_ROOT%{_ulibdir}/lib%{name}%{version}.so
fi

ln -sf %{_libdir}/lib%{name}%{version}.so $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so

install -d $RPM_BUILD_ROOT%{_mandir}/man{n,3}
install doc/*.n $RPM_BUILD_ROOT%{_mandir}/mann
install doc/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

# Rename conflicting manpages.
for i in $RPM_BUILD_ROOT%{_mandir}/mann/*.n
do
	mv $i $RPM_BUILD_ROOT%{_mandir}/mann/ttk::`basename $i`
done

cp -a demos $RPM_BUILD_ROOT%{_ulibdir}/%{name}%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib%{name}%{version}.so
%dir %{_ulibdir}/%{name}%{version}
%{_ulibdir}/%{name}%{version}/*.tcl
%if "%{_lib}" != "lib"
%{_ulibdir}/lib*%{version}.so
%endif
%{_mandir}/mann/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib%{name}.so
%{_libdir}/libttkstub.a
%{_includedir}/*
%{_mandir}/man3/*

%files demo
%defattr(644,root,root,755)
%{_ulibdir}/%{name}%{version}/demos
