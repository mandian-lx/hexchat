Summary:   A popular and easy to use graphical IRC (chat) client
Name:      hexchat
Version:   2.9.5
Release:   1%{?dist}
Group:     Applications/Internet
License:   GPLv2+
URL:       http://www.hexchat.org
Source:    http://dl.hexchat.org/hexchat/%{name}-%{version}.tar.xz

BuildRequires: perl-ExtUtils-Embed, python-devel, pciutils-devel
BuildRequires: dbus-glib-devel, intltool, libtool
BuildRequires: glib2-devel, gtk2-devel
BuildRequires: libproxy-devel, libsexy-devel, libnotify-devel, openssl-devel
BuildRequires: desktop-file-utils, hicolor-icon-theme

%description
HexChat is an easy to use graphical IRC chat client for the X Window System.
It allows you to join multiple IRC channels (chat rooms) at the same time, 
talk publicly, private one-on-one conversations etc. Even file transfers
are possible.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
%configure --enable-spell=libsexy

make %{?_smp_mflags} V=1

%install
make DESTDIR=%{buildroot} install

# Get rid of libtool archives
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Remove include, not worth a -devel package
rm -f %{buildroot}%{_includedir}/hexchat-plugin.h

# Remove unused schema
rm -f %{buildroot}%{_sysconfdir}/gconf/schemas/apps_hexchat_url_handler.schemas

# Fix opening irc:// links by adding mimetype and editing exec
desktop-file-install \
    --add-mime-type='x-scheme-handler/irc;x-scheme-handler/ircs' \
    --remove-key=Exec \
    --dir=%{buildroot}%{_datadir}/applications/ \
    %{buildroot}%{_datadir}/applications/hexchat.desktop

# Workaround for EL's version of desktop-file-install
echo Exec="sh -c \"hexchat --existing --url %u || exec hexchat\"">>%{buildroot}%{_datadir}/applications/hexchat.desktop

%find_lang %{name}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%{_bindir}/hexchat
%doc share/doc/*
%dir %{_libdir}/hexchat
%dir %{_libdir}/hexchat/plugins
%{_libdir}/hexchat/plugins/checksum.so
%{_libdir}/hexchat/plugins/doat.so
%{_libdir}/hexchat/plugins/fishlim.so
%{_libdir}/hexchat/plugins/sysinfo.so
%{_libdir}/hexchat/plugins/perl.so
%{_libdir}/hexchat/plugins/python.so
%{_datadir}/applications/hexchat.desktop
%{_datadir}/icons/hicolor/*
%{_datadir}/dbus-1/services/org.hexchat.service.service
%{_mandir}/man1/*.gz

%changelog
* Mon Apr 1 2013 TingPing <tingping@tingping.se> - 2.9.5-1
- Version bump to 2.9.5

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 27 2012 TingPing <tingping@tingping.se> - 2.9.4-1
- Initial HexChat package
