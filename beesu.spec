%define nbmversion 1.7

Summary:	Graphical wrapper for su
Name:		beesu
Version:	2.7
Release:	2
License:	GPLv2+
Group:		System/Base
Url:		http://www.honeybeenet.altervista.org
Source0:	http://honeybeenet.altervista.org/beesu/files/beesu-sources/%{name}-%{version}.tar.bz2
Source1:	http://honeybeenet.altervista.org/beesu/files/beesu-manager/nautilus-beesu-manager-%{nbmversion}.tar.bz2
Patch1:		beesu-nautilus-no-browser.patch
Requires:	pam
Requires:	usermode

%description
Beesu is a wrapper around su and works with consolehelper to let you
have a graphic interface like gksu.

%package -n nautilus-beesu-manager
Summary:	Utility to add beesu scripts to nautilus
Version:	%{nbmversion}
Group:		Graphical desktop/Other
Requires:	beesu
Requires:	zenity
Requires:	nautilus
BuildArch:	noarch

%description -n nautilus-beesu-manager
nautilus-beesu-manager is a little utility to add some useful scripts
to the Nautilus file browser; nautilus-beesu-manager can add scripts
to Nautilus using beesu to elevate the user's privileges to root.

%prep
%setup -q -a1
chmod -x nautilus-beesu-manager-%{nbmversion}/COPYING nautilus-beesu-manager-%{nbmversion}/README
%patch1 -p1

%build
%make CFLAGS="%{optflags} -fno-delete-null-pointer-checks"

%install
mkdir -p %{buildroot}%{_datadir}/%{name}

%makeinstall_std

#nbm
pushd nautilus-beesu-manager-%{nbmversion}
mkdir -v -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/
mkdir -v -p %{buildroot}%{_datadir}/applications/
install -p -m 755 nautilus-beesu-manager %{buildroot}%{_bindir}
install -p -m 644 nautilus-beesu-manager.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/
desktop-file-install --dir %{buildroot}%{_datadir}/applications --mode 0644 nautilus-beesu-manager.desktop
mkdir -v -p %{buildroot}%{_libexecdir}/nautilus-beesu-manager/
install -p -m 755 libexec/api %{buildroot}%{_libexecdir}/nautilus-beesu-manager/
cp -a libexec/scripts %{buildroot}%{_libexecdir}/nautilus-beesu-manager/
install -p -m 644 libexec/local-launcher %{buildroot}%{_libexecdir}/nautilus-beesu-manager/
popd

%files
%doc COPYING README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%{_sysconfdir}/profile.d/%{name}-bash-completion.sh
%{_sbindir}/%{name}
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.xz

%files -n nautilus-beesu-manager
%doc nautilus-beesu-manager-%{nbmversion}/COPYING nautilus-beesu-manager-%{nbmversion}/README
%{_bindir}/nautilus-beesu-manager
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/32x32/apps/nautilus-beesu-manager.png
%{_libexecdir}/nautilus-beesu-manager/

