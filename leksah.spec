# https://fedoraproject.org/wiki/Packaging:Haskell

%global ghc_without_dynamic 1
%global ghc_without_shared 1
%global without_prof 1
%global without_haddock 1

%global pkg_name leksah

%bcond_with tests

Name:           %{pkg_name}
Version:        0.14.4.0
Release:        1%{?dist}
Summary:        Haskell IDE

# LICENSE file is GPLv2 while sources only mention GPL, hence GPL+.
License:        GPL+
Url:            https://hackage.haskell.org/package/%{name}
Source0:        https://hackage.haskell.org/package/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
Source2:        %{name}_loadsession.desktop
Source3:        %{name}.xml
#Patch1:         leksah-0.14-gtk.patch
Patch2:         leksah-0.14-no-hamlet.patch

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  chrpath
BuildRequires:  ghc-QuickCheck-devel
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-binary-devel
BuildRequires:  ghc-binary-shared-devel
BuildRequires:  ghc-blaze-html-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-conduit-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-deepseq-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-executable-path-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-ghc-devel
#BuildRequires:  ghc-ghcjs-codemirror-devel
#BuildRequires:  ghc-ghcjs-dom-devel
BuildRequires:  ghc-gio-devel
#BuildRequires:  ghc-glib-devel
#BuildRequires:  ghc-gtk3-devel
#BuildRequires:  ghc-gtksourceview3-devel
BuildRequires:  ghc-haskell-src-exts-devel
BuildRequires:  ghc-hgettext-devel
BuildRequires:  ghc-hlint-devel
BuildRequires:  ghc-hslogger-devel
#BuildRequires:  ghc-jsaddle-devel
BuildRequires:  ghc-leksah-server-devel
#BuildRequires:  ghc-lens-devel
#BuildRequires:  ghc-ltk-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-network-devel
BuildRequires:  ghc-old-time-devel
BuildRequires:  ghc-parsec-devel
BuildRequires:  ghc-pretty-devel
#BuildRequires:  ghc-pretty-show-devel
BuildRequires:  ghc-regex-base-devel
BuildRequires:  ghc-regex-tdfa-devel
#BuildRequires:  ghc-regex-tdfa-text-devel
BuildRequires:  ghc-setlocale-devel
BuildRequires:  ghc-shakespeare-devel
BuildRequires:  ghc-strict-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-transformers-devel
BuildRequires:  ghc-unix-devel
BuildRequires:  ghc-utf8-string-devel
#BuildRequires:  ghc-vado-devel
#BuildRequires:  ghc-vcsgui-devel
#BuildRequires:  ghc-vcswrapper-devel
#BuildRequires:  ghc-webkitgtk3-devel
#BuildRequires:  ghc-webkit-javascriptcore-devel
%if %{with tests}
BuildRequires:  ghc-monad-loops-devel
%endif
# End cabal-rpm deps
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Requires:       leksah-server
BuildRequires:  cabal-install > 1.18
# for pretty-show
BuildRequires:  happy
BuildRequires:  gtk2hs-buildtools
BuildRequires:  pkgconfig(webkitgtk-3.0)
BuildRequires:  pkgconfig(gtksourceview-3.0)

%description
Leksah is an Integrated Development Environment for
Haskell written in Haskell and using the GTK+ GUI Toolkit.



%prep
%setup -q
%patch2 -p1 -b .orig
cabal-tweak-flag dyre False
#cabal-tweak-flag gtk3 False
cabal-tweak-flag loc True
cabal-tweak-flag network-uri False


%build
%global cabal cabal
[ -d "$HOME/.cabal" ] || %cabal update
%cabal sandbox init
# for haddock-library hGetContents
export LANG=en_US.utf8
# for gcc 5
cat > cabal.config << EOF
constraints: webkitgtk3 >= 0.13.1.3
EOF
%cabal install --only-dependencies --force-reinstalls
%ghc_bin_build


%install
%ghc_bin_install
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/128x128/apps
install --mode=0644 -D pics/leksah.png %{buildroot}/%{_datadir}/icons/hicolor/128x128/apps/leksah.png
desktop-file-install --add-category="Development"  --add-category="X-DevelopmentTools" --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}
desktop-file-install --add-category="Development"  --add-category="X-DevelopmentTools" --dir=%{buildroot}%{_datadir}/applications %{SOURCE2}
# Copy mime file
mkdir -p %{buildroot}/%{_datadir}/mime/packages
install --mode=0644 -D %{SOURCE3} %{buildroot}/%{_datadir}/mime/packages

rm -rf %{buildroot}%ghclibdir


%check
%if %{with tests}
%cabal test
%endif


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    touch --no-create %{_datadir}/mime/packages &> /dev/null || :
    update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :



%files
%doc LICENSE
%doc Readme.md doc
%{_bindir}/bewleksah
%{_bindir}/%{name}
%{_datadir}/%{name}-%{version}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}_loadsession.desktop
%{_datadir}/mime/packages/leksah.xml
%{_datadir}/icons/hicolor/128x128/apps/leksah.png


%changelog
* Tue Mar 03 2015 Jens Petersen <petersen@redhat.com> - 0.14.4.0-1
- update to 0.14.4.0
- patch out hamlet
- build with cabal-install

* Thu Oct 02 2014 Rex Dieter <rdieter@fedoraproject.org> 0.14.0.1-2
- update mime scriptlet

* Tue Sep 16 2014 Jens Petersen <petersen@redhat.com> - 0.14.0.1-1
- update to 0.14.0.1
- disable network-uri

* Wed Sep 03 2014 Jens Petersen <petersen@redhat.com> - 0.13.4.3-1
- update to 0.13.4.3
- needs new deps: vado, vcsgui, vcswrapper

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 16 2014 Jens Petersen <petersen@redhat.com> - 0.12.1.3-15
- update to cblrpm-0.8.11 and enable tests
- disable testsuite on ARM since it doesn't link

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
- Bring back deps.patch to fix bug #863499. Without this patch, leksah binary
  depends on its shared library. Loader is not able to resolve this at runtime
  because the rpath information for leksah shared library is incorrect.

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
