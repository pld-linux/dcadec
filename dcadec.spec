#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Free DTS Coherent Acoustics decoder with support for HD extensions
Summary(pl.UTF-8):	Wolnodostępny dekoder DTS Coherent Acoustics z obsługą rozszerzeń HD
Name:		dcadec
# see Makefile
Version:	0.0.0
%define	snap	20150606
%define	gitref	2a9186e34ce557d3af1a20f5b558d1e6687708b9
Release:	0.%{snap}.1
License:	LGPL v2.1+
Group:		Applications/Sound
Source0:	https://github.com/foo86/dcadec/archive/2a9186e34ce557d3af1a20f5b558d1e6687708b9/%{name}-%{snap}.tar.gz
# Source0-md5:	37df95f78aa614ef1adbadc6b466c4b4
URL:		https://github.com/foo86/dcadec
Requires:	%{name}-libs = %{version}-%{release}
# dcadec binary
Conflicts:	libdts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
dcadec is a free DTS Coherent Acoustics decoder with support for HD
extensions.

Supported features:
- Decoding of standard DTS core streams with up to 5.1 channels
- Decoding of DTS-ES streams with discrete back channel
- Decoding of High Resolution streams with up to 7.1 channels and
  extended bitrate
- Decoding of 96/24 core streams
- Lossless decoding of Master Audio streams with up to 7.1 channels, 192
  kHz
- Downmixing to stereo and 5.1 using embedded coefficients

Features not implemented:
- Decoding of DTS Express streams
- Applying dynamic range compression and dialog normalization

%description -l pl.UTF-8
dcadec to wolnodostępny dekoder formatu DTS Coherent Acoustics z
obsługą rozszerzeń HD.

Obsługiwane:
- dekodowanie standardowych strumieni podstawowych DTS o liczbie
  kanałów do 5.1
- dekodowanie strumieni DTS-ES z dyskretnym kanałem tylnym
- dekodowanie strumieni HD o liczbie kanałów do 7.1 z rozszerzoną
  prędkością bitową
- dekodowanie strumieni podstawowych 96/24
- bezstratne dekodowanie strumieni Master Audio o liczbie kanałów do
  7.1, do 192 kHz
- miksowanie w dół do stereo i 5.1 przy użyciu wbudowanych
  współczynników

Nie obsługiwane:
- dekodowanie strumieni DTS Express
- wykonywanie kompresji dynamiki oraz normalizacja dialogów

%package libs
Summary:	Free DTS Coherent Acoustics decoder library with support for HD extensions
Summary(pl.UTF-8):	Wolnodostępna biblioteka dekodera DTS Coherent Acoustics z obsługą rozszerzeń HD
Group:		Libraries

%description libs
libdcadec is a free DTS Coherent Acoustics decoder library with
support for HD extensions.

Supported features:
- Decoding of standard DTS core streams with up to 5.1 channels
- Decoding of DTS-ES streams with discrete back channel
- Decoding of High Resolution streams with up to 7.1 channels and
  extended bitrate
- Decoding of 96/24 core streams
- Lossless decoding of Master Audio streams with up to 7.1 channels, 192
  kHz
- Downmixing to stereo and 5.1 using embedded coefficients

Features not implemented:
- Decoding of DTS Express streams
- Applying dynamic range compression and dialog normalization

%description libs -l pl.UTF-8
libdcadec to wolnodostępna biblioteka dekodera formatu DTS Coherent
Acoustics z obsługą rozszerzeń HD.

Obsługiwane:
- dekodowanie standardowych strumieni podstawowych DTS o liczbie
  kanałów do 5.1
- dekodowanie strumieni DTS-ES z dyskretnym kanałem tylnym
- dekodowanie strumieni HD o liczbie kanałów do 7.1 z rozszerzoną
  prędkością bitową
- dekodowanie strumieni podstawowych 96/24
- bezstratne dekodowanie strumieni Master Audio o liczbie kanałów do
  7.1, do 192 kHz
- miksowanie w dół do stereo i 5.1 przy użyciu wbudowanych
  współczynników

Nie obsługiwane:
- dekodowanie strumieni DTS Express
- wykonywanie kompresji dynamiki oraz normalizacja dialogów

%package devel
Summary:	Header files for libdcadec library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libdcadec
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for libdcadec library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libdcadec.

%package static
Summary:	Static libdcadec library
Summary(pl.UTF-8):	Statyczna biblioteka libdcadec
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libdcadec library.

%description static -l pl.UTF-8
Statyczna biblioteka libdcadec.

%prep
%setup -q -n %{name}-%{gitref}

%build
CFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make} all \
	CC="%{__cc}" \
	CONFIG_SHARED=1 \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir}

%if %{with static_libs}
%{__make} libdcadec/libdcadec.a
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	CONFIG_SHARED=1 \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir}

%if %{with static_libs}
cp -p libdcadec/libdcadec.a $RPM_BUILD_ROOT%{_libdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/dcadec

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdcadec.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/libdcadec
%{_pkgconfigdir}/dcadec.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdcadec.a
%endif
