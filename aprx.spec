Name:           aprx
Version:        2.9.0
Release:        1
Summary:        Hamradio APRS iGate / Digipeater
License:        BSD
URL:            http://thelifeofkenneth.com/aprx/
Source0:        https://github.com/PhirePhly/aprx/archive/v%{version}.zip

Patch0:		https://raw.githubusercontent.com/peterfromthehill/aprx-rpm/master/aprx-%{version}-fix-missing-now-from-aprx-stat.patch

BuildRequires:  systemd-units

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service 

%description
Aprx is an APRS iGate that has minimal system requirements. It can handle
an arbitrary number of radio modems, optionally relay APRS packets from radio
to the APRS-IS network, optionally digipeat AX25 with or without NEWn-N
rules, optionally relay APRS packets from APRS-IS to radio (TX-iGate)

%prep
%setup -q
%patch0 -p1

%build
%configure --with-erlangstorage 
make %{?_smp_mflags}
make logrotate.aprx

%install
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
mkdir -p $RPM_BUILD_ROOT/var/log/aprx

make install DESTDIR=$RPM_BUILD_ROOT

install -m 644 logrotate.aprx   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/aprx
install -m 644 rpm/aprx.default $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/aprx

%if 0%{?rhel} >= 7 || 0%{?fedora} >= 16
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -m 644 rpm/aprx.service $RPM_BUILD_ROOT%{_unitdir}/%{name}.service
%else
mkdir -p $RPM_BUILD_ROOT%{_initddir}
install -m 755 rpm/aprx.init    $RPM_BUILD_ROOT%{_initddir}/aprx
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
# INSTALL not bundled
%doc LICENSE README TODO PROTOCOLS
%doc ChangeLog
%doc aprx.conf aprx-complex.conf
%doc doc/aprx-manual.pdf
%doc ViscousDigipeater.README ViscousDigipeaterTxEffect.png
%dir /var/log/aprx
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/aprx.conf
%config(noreplace) %{_sysconfdir}/sysconfig/aprx
%config(noreplace) %{_sysconfdir}/logrotate.d/aprx
%{_sbindir}/aprx
%{_sbindir}/aprx-stat
%doc %{_mandir}/man8/aprx.8.gz
%doc %{_mandir}/man8/aprx-stat.8.gz


%changelog
* Sun Sep 03 2017 Michael Haupt <peter@1qay.net> - v%{version}-%{release}
- Add fix c877195

* Thu Oct 11 2012 Andrew Elwell <Andrew.Elwell@gmail.com> - v%{version}
- Packaging for Fedora

* Sat Jan 12 2008 Matti Aarnio - OH2MQK - KP20NG <oh2mqk@sral.fi> - 
- RPM framework added
