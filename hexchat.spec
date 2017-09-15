%define _disable_lto 1

Summary:	A popular and easy to use graphical IRC (chat) client
Name:		hexchat
Version:	2.12.4
Release:	1
Group:		Networking/IRC
License:	GPLv2+
URL:		https://hexchat.github.io
Source0:	https://dl.hexchat.net/hexchat/%{name}-%{version}.tar.xz

BuildRequires:	autoconf-archive
BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	gettext-devel
BuildRequires:	perl-devel
BuildRequires:	tcl-devel
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libproxy-1.0)
BuildRequires:	pkgconfig(libsexy)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(python3)
BuildRequires:	openssl-devel

%description
HexChat is an easy to use graphical IRC chat client for the X Window System.
It allows you to join multiple IRC channels (chat rooms) at the same time, 
talk publicly, private one-on-one conversations etc. Even file transfers
are possible.

%prep
%setup -q

%files -f %{name}.lang
%doc readme.md
%{_bindir}/%{name}
%{_bindir}/%{name}-text
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/checksum.so
%{_libdir}/%{name}/plugins/fishlim.so
%{_libdir}/%{name}/plugins/lua.so
%{_libdir}/%{name}/plugins/perl.so
%{_libdir}/%{name}/plugins/python.so
%{_libdir}/%{name}/plugins/sysinfo.so
%{_iconsdir}/hicolor/*/apps/*.*g
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/dbus-1/services/org.hexchat.service.service
%{_mandir}/man1/%{name}.1.*

#---------------------------------------------------------------------------

%build
%global optflags %{optflags} -flto

sh ./autogen.sh
%configure \
	--enable-python=python3 \
	--enable-static-analysis \
	--enable-textfe \
	%{nil}
%make

%install
%makeinstall_std

# Add SVG for hicolor
install -dm 0755 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
install -pm 0644 data/icons/%{name}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/

# Fix opening irc:// links by adding mimetype and editing exec
desktop-file-edit \
	--add-mime-type='x-scheme-handler/irc;x-scheme-handler/ircs' \
	--set-key=Exec \
	--set-value="sh -c \"hexchat --existing --url %U || exec hexchat\"" \
	%{buildroot}%{_datadir}/applications/%{name}.desktop

# Get rid of libtool archives
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Drop deprecated TCL plugin
find %{buildroot} -name 'tcl.so' -exec rm -f {} ';'

# Remove unused schema
rm -f %{buildroot}%{_sysconfdir}/gconf/schemas/apps_hexchat_url_handler.schemas


#(tpg) remove these files
rm -rf %{buildroot}%{_includedir}/hexchat-plugin.h
rm -rf %{buildroot}%{_libdir}/pkgconfig/hexchat-plugin.pc

# locales
%find_lang %{name}

