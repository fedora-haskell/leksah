# For Haskell Packaging Guidelines see:
# - https://fedoraproject.org/wiki/Packaging:Haskell
# - https://fedoraproject.org/wiki/PackagingDrafts/Haskell

%global pkg_name leksah

# common part of summary for all the subpackages
%global common_summary An IDE for Haskell

# main description used for all the subpackages
%global common_description Leksah is an Integrated Development Environment for \
Haskell written in Haskell. Leksah uses GTK+ as GUI Toolkit.

Name:           %{pkg_name}
Version:        0.10.0.4
Release:        6%{?dist}.1
Summary:        Haskell IDE
Group:          Development/Tools
# LICENSE file is GPLv2 while sources only mention GPL, hence GPL+.
License:        GPL+
URL:            http://hackage.haskell.org/package/%{name}
Source0:        http://hackage.haskell.org/packages/archive/%{name}/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
Source2:        %{name}_loadsession.desktop
Source3:        %{name}.xml
ExclusiveArch:  %{ghc_arches}
BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
%if %{undefined without_hscolour}
BuildRequires:  hscolour
%endif
# END: cabal2spec-0.24
# BR any C devel dependency here
# list ghc-*-prof dependencies:
BuildRequires:  ghc-Cabal-prof, ghc-directory-prof, ghc-gtksourceview2-prof, ghc-old-time-prof, ghc-process-leksah-prof, ghc-regex-tdfa-prof, ghc-utf8-string-prof, ghc-time-prof, ghc-ltk-prof, ghc-binary-shared-prof, ghc-deepseq-prof, ghc-hslogger-prof, ghc-leksah-server-prof, ghc-network-prof, ghc-ghc-prof, ghc-strict-prof
BuildRequires: desktop-file-utils
# all requires list
Requires: hicolor-icon-theme
Requires: leksah-server

# patches
Patch1 : leksah_dep.patch

%description
%{common_description}


%if %{undefined ghc_without_shared}
%package -n ghc-%{pkg_name}
Summary:        Development files for %{common_summary}
Group:          Development/Libraries
# BEGIN: cabal2spec-0.24
%{?ghc_devel_requires}
Obsoletes:      ghc-%{pkg_name}-prof < %{version}-%{release}
Provides:       ghc-%{pkg_name}-prof = %{version}-%{release}
# END: cabal2spec-0.24
# remember to require any C devel dependency here
# Haskell devel dependencies are autogenerated by ghc-deps.sh

%description -n ghc-%{pkg_name}
%{common_description}

This package contains the shared library.
%endif


%package -n ghc-%{pkg_name}-devel
Summary:        Development files for %{common_summary}
Group:          Development/Libraries
# BEGIN: cabal2spec-0.24
%{?ghc_devel_requires}
Obsoletes:      ghc-%{pkg_name}-prof < %{version}-%{release}
Provides:       ghc-%{pkg_name}-prof = %{version}-%{release}
# END: cabal2spec-0.24
# remember to require any C devel dependency here
# Haskell devel dependencies are autogenerated by ghc-deps.sh

%description -n ghc-%{pkg_name}-devel
%{common_description}

This package contains the development files.


%prep
%setup -q
%patch1 -p1 -b .orig


%build
%ghc_lib_build


%install
%ghc_lib_install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/128x128/apps
install --mode=0644 -D pics/leksah.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/128x128/apps/leksah.png
desktop-file-install --add-category="Development"  --add-category="X-DevelopmentTools" --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}
desktop-file-install --add-category="Development"  --add-category="X-DevelopmentTools" --dir=%{buildroot}%{_datadir}/applications %{SOURCE2}
# Copy mime file
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/mime/packages
install --mode=0644 -D %{SOURCE3} $RPM_BUILD_ROOT/%{_datadir}/mime/packages

%post -n ghc-%{pkg_name}-devel
%ghc_pkg_recache


%postun -n ghc-%{pkg_name}-devel
%ghc_pkg_recache


%files
%doc LICENSE
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_datadir}/%{name}-%{version}
%dir %{_datadir}/%{name}-%{version}/data
%dir %{_datadir}/%{name}-%{version}/pics
%attr(644,root,root) %{_datadir}/%{name}-%{version}/LICENSE
%attr(644,root,root) %{_datadir}/%{name}-%{version}/Readme
%attr(644,root,root) %{_datadir}/%{name}-%{version}/pics/*
%attr(644,root,root) %{_datadir}/%{name}-%{version}/data/*
%attr(644,root,root) %{_datadir}/applications/%{name}.desktop
%attr(644,root,root) %{_datadir}/applications/%{name}_loadsession.desktop
%attr(644,root,root) %{_datadir}/mime/packages/leksah.xml
%attr(644,root,root) %{_datadir}/icons/hicolor/128x128/apps/leksah.png


%if %{undefined ghc_without_shared}
%files -n ghc-%{pkg_name} -f ghc-%{pkg_name}.files
%endif


%files -n ghc-%{pkg_name}-devel -f ghc-%{pkg_name}-devel.files


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%changelog
* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 0.10.0.4-6.1
- rebuild with new gmp

* Mon Oct 10 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.10.0.4-6
- Fix bug 744559.
- Added leksah.xml to mime database.

* Sun Sep 25 2011  Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.10.0.4-5
- Upgrade to cabal2spec-0.24.1
- Rebuild for gtk2hs updates

* Sun Aug 28 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.10.0.4-4
- Rebuild for ghc-hslogger update to 1.1.5

* Sat Jul 2 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.10.0.4-3
- Added license comment before License field.
- Fixed vertical spacing.
- Modified BuildRequires (as per Jens' suggestion) so that its a closure of the dependencies mentioned in the cabal file.

* Sun Jun 26 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.10.0.4-2
- Upgrade to cabal2spec-0.23.2
- License in the LICENSE file is mentioned as GPLV2 while sources specify license as GPL.Hence GPL+.

* Sun Jun 12 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.10.0.4-1
- Upgrade to 0.10.0.4. Update to cabal2spec-0.22.7
- Removed desktop_file.patch.
- Patched cabal file to workaround cabal bug @ http://hackage.haskell.org/trac/hackage/ticket/656

* Sun Apr 17 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.10.0.1-1
- upgrade to 0.10.0.1, update to cabal2spec-0.22.5.

* Sun Jan 30 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.8.0.8-1
- updated dependencies. 
- generate desktop file. scale icon file to 64x64. run gtk-update-icon-cache after transaction

* Sun Jan 30 2011 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.8.0.8-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.4
