# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name leksah

Name:           %{pkg_name}
Version:        0.12.1.3
Release:        15%{?dist}
Summary:        Haskell IDE

# LICENSE file is GPLv2 while sources only mention GPL, hence GPL+.
License:        GPL+
URL:            http://hackage.haskell.org/package/%{name}
Source0:        http://hackage.haskell.org/packages/archive/%{name}/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
Source2:        %{name}_loadsession.desktop
Source3:        %{name}.xml
Patch1:         haddock.patch
Patch2:         leksah-0.12.1-ghc-7.6.patch

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-QuickCheck-devel
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-binary-devel
BuildRequires:  ghc-binary-shared-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-deepseq-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-enumerator-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-ghc-devel
BuildRequires:  ghc-gio-devel
BuildRequires:  ghc-glib-devel
BuildRequires:  ghc-gtk-devel
BuildRequires:  ghc-gtksourceview2-devel
BuildRequires:  ghc-hslogger-devel
BuildRequires:  ghc-leksah-server-devel
BuildRequires:  ghc-ltk-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-network-devel
BuildRequires:  ghc-old-time-devel
BuildRequires:  ghc-parsec-devel
BuildRequires:  ghc-pretty-devel
BuildRequires:  ghc-regex-base-devel
BuildRequires:  ghc-regex-tdfa-devel
BuildRequires:  ghc-strict-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-transformers-devel
BuildRequires:  ghc-unix-devel
BuildRequires:  ghc-utf8-string-devel
# End cabal-rpm deps
BuildRequires:  desktop-file-utils
BuildRequires:  chrpath
Requires:       hicolor-icon-theme
Requires:       leksah-server

%description
Leksah is an Integrated Development Environment for
Haskell written in Haskell. Leksah uses GTK+ as GUI Toolkit.


%package -n ghc-%{name}
Summary:        Haskell %{name} library

%description -n ghc-%{name}
This package provides the Haskell %{name} shared library.


%package -n ghc-%{name}-devel
Summary:        Haskell %{name} library development files
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       ghc-%{name} = %{version}-%{release}

%description -n ghc-%{name}-devel
This package provides the Haskell %{name} library development files.


%prep
%setup -q
%patch1 -p1 -b .orig
%patch2 -p1 -b .orig

cabal-tweak-dep-ver Cabal "<1.15" "<1.17"
cabal-tweak-dep-ver QuickCheck "<2.5" "<2.7"
cabal-tweak-dep-ver base "<4.6" "<4.7"
cabal-tweak-dep-ver bytestring "<0.10" "<0.11"
cabal-tweak-dep-ver containers "<0.5" "<0.6"
cabal-tweak-dep-ver ghc "<7.5" "<7.7"
cabal-tweak-dep-ver hslogger "<1.2" "<1.3"
cabal-tweak-dep-ver unix "<2.6" "<2.7"


%build
%ghc_lib_build


%install
%ghc_lib_install
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/128x128/apps
install --mode=0644 -D pics/leksah.png %{buildroot}/%{_datadir}/icons/hicolor/128x128/apps/leksah.png
desktop-file-install --add-category="Development"  --add-category="X-DevelopmentTools" --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}
desktop-file-install --add-category="Development"  --add-category="X-DevelopmentTools" --dir=%{buildroot}%{_datadir}/applications %{SOURCE2}
# Copy mime file
mkdir -p %{buildroot}/%{_datadir}/mime/packages
install --mode=0644 -D %{SOURCE3} %{buildroot}/%{_datadir}/mime/packages

%ghc_fix_dynamic_rpath %{name}


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


%post -n ghc-%{name}-devel
%ghc_pkg_recache


%postun -n ghc-%{name}-devel
%ghc_pkg_recache


%files
%doc LICENSE Readme
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_datadir}/%{name}-%{version}
%dir %{_datadir}/%{name}-%{version}/data
%dir %{_datadir}/%{name}-%{version}/data/leksah-welcome
%dir %{_datadir}/%{name}-%{version}/data/leksah-welcome/src
%dir %{_datadir}/%{name}-%{version}/pics
%dir %{_datadir}/%{name}-%{version}/language-specs
%attr(644,root,root) %{_datadir}/%{name}-%{version}/LICENSE
%attr(644,root,root) %{_datadir}/%{name}-%{version}/Readme
%attr(644,root,root) %{_datadir}/%{name}-%{version}/pics/*
%attr(644,root,root) %{_datadir}/%{name}-%{version}/data/*.lksh*
%attr(644,root,root) %{_datadir}/%{name}-%{version}/data/leksah.menu
%attr(644,root,root) %{_datadir}/%{name}-%{version}/data/LICENSE
%attr(644,root,root) %{_datadir}/%{name}-%{version}/data/welcome.txt
%attr(644,root,root) %{_datadir}/%{name}-%{version}/data/leksah-welcome/*.*
%attr(644,root,root) %{_datadir}/%{name}-%{version}/data/leksah-welcome/src/Main.hs
%attr(644,root,root) %{_datadir}/%{name}-%{version}/language-specs/*
%attr(644,root,root) %{_datadir}/applications/%{name}.desktop
%attr(644,root,root) %{_datadir}/applications/%{name}_loadsession.desktop
%attr(644,root,root) %{_datadir}/mime/packages/leksah.xml
%attr(644,root,root) %{_datadir}/icons/hicolor/128x128/apps/leksah.png


%files -n ghc-%{name} -f ghc-%{name}.files
%doc LICENSE


%files -n ghc-%{name}-devel -f ghc-%{name}-devel.files


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Jens Petersen <petersen@redhat.com> - 0.12.1.3-14
- rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul  4 2013 Jens Petersen <petersen@redhat.com> - 0.12.1.3-12
- ghc_fix_dynamic_rpath needs BR chrpath (#981010)

* Mon Jun 10 2013 Jens Petersen <petersen@redhat.com> - 0.12.1.3-11
- update to new simplified Haskell Packaging Guidelines
- patch from git for ghc-7.6

* Sat Feb 23 2013 Kevin Fenzi <kevin@scrye.com> - 0.12.1.3-10
- Rebuild for broken deps in rawhide

* Wed Jan 30 2013 Jens Petersen <petersen@redhat.com> - 0.12.1.3-9
- drop deps.patch and link leksah against itself
- use new ghc_fix_dynamic_rpath macro

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.12.1.3-8
- update with cabal-rpm

* Mon Oct 29 2012 Jens Petersen <petersen@redhat.com> - 0.12.1.3-7
- allow building with QuickCheck 2.5

* Fri Oct 12 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.12.1.3-6
- Bring back deps.patch to fix bug #863499 . Without this patch, leksah binary depends \
on its shared library. Loader is not able to resolve this at runtime because \
the rpath information for leksah shared library is incorrect.

* Tue Oct 02 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.12.1.3-5
- Rebuild for ghc-7.4.1

* Sat Aug 11 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.12.1.3-4
- Rebuild for libffi

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.12.1.3-2
- change prof BRs to devel

* Fri Jun 29 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.12.1.3-1
- update to 0.12.1.3

* Fri Jun 22 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.12.1.2-1
- update to 0.12.1.2
- haddock.patch is not needed
- update files section and list the folders/files under data folder properly. wildcard * makes everthing 644, including folders

* Sun Jun 10 2012 Jens Petersen <petersen@redhat.com> - 0.12.1.0-1
- update to 0.12.1.0
- deps patch is no longer needed

* Tue Mar 20 2012 Jens Petersen <petersen@redhat.com> - 0.12.0.3-3
- update to cabal2spec-0.25
- drop unnecessary depends on process-leksah

* Sun Mar 18 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.12.0.3-2
- Rebuild for leksah-server update

* Mon Mar 12 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.12.0.3-1
- Package update to 0.12.0.3
- Added patches for reducing version requirement of QuickCheck and fixing issue when
- running haddock

* Sun Jan 08 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.10.0.4-7
- Rebuild for haskell-platform

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.10.0.4-6.2
- rebuild with new gmp without compat lib

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
