%global commit0 ac1703e9d7feebbf5443a986e08332b1e1c5afcf
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global foundry twitter
%global fontname twemoji
%global Fontname Twemoji


Name:           %{foundry}-%{fontname}-fonts
Version:        13.0.2
Release:        1%{?dist}
Summary:        Twitter Emoji for everyone

# In noto-emoji-fonts source
## noto-emoji code is in ASL 2.0 license
## Emoji fonts are under OFL license
### third_party color-emoji code is in BSD license
### third_party region-flags code is in Public Domain license
# In twemoji source
## Artwork is Creative Commons Attribution 4.0 International
## Non-artwork is MIT
License:        OFL and ASL 2.0 and CC-BY and MIT
URL:            https://twemoji.twitter.com/
Source0:        https://github.com/googlei18n/noto-emoji/archive/%{commit0}.tar.gz#/noto-emoji-%{shortcommit0}.tar.gz
Source2:        com.%{foundry}.%{fontname}.metainfo.xml
Source4:        https://github.com/%{foundry}/%{fontname}/archive/v%{version}.tar.gz#/%{fontname}-%{version}.tar.gz

Patch0:         noto-emoji-use-system-pngquant.patch
Patch1:         noto-emoji-build-all-flags.patch
Patch2:         noto-emoji-use-gm.patch

BuildArch:      noarch
BuildRequires: make
BuildRequires:  GraphicsMagick
BuildRequires:  cairo-devel
BuildRequires:  fontpackages-devel
BuildRequires:  fonttools
BuildRequires:  libappstream-glib
BuildRequires:  nototools
BuildRequires:  pngquant
BuildRequires:  python3-devel
BuildRequires:  python3dist(fonttools)
BuildRequires:  zopfli

Requires:       fontpackages-filesystem


%description
A color emoji font with a flat visual style, designed and used by Twitter.


%prep
%autosetup -p1 -n noto-emoji-%{commit0}
rm -rf third_party/pngquant
mv LICENSE LICENSE-BUILD

tar -xf %{SOURCE4}
sed 's/Noto Color Emoji/Twemoji/; s/NotoColorEmoji/Twemoji/; s/Copyright .* Google Inc\./Twitter, Inc and other contributors./; s/ Version .*/ %{version}/; s/.*is a trademark.*//; s/Google, Inc\./Twitter, Inc and other contributors/; s,http://www.google.com/get/noto/,https://github.com/twitter/twemoji/,; s/.*is licensed under.*/      Creative Commons Attribution 4.0 International/; s,http://scripts.sil.org/OFL,http://creativecommons.org/licenses/by/4.0/,' NotoColorEmoji.tmpl.ttx.tmpl > Twemoji.tmpl.ttx.tmpl
pushd %{fontname}-%{version}/assets/72x72/
for png in *.png; do
    mv $png emoji_u${png//-/_}
done
popd


%build
make %{?_smp_mflags} OPT_CFLAGS="$RPM_OPT_FLAGS" EMOJI=%{Fontname} EMOJI_SRC_DIR=%{fontname}-%{version}/assets/72x72 FLAGS= BODY_DIMENSIONS=76x72


%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p %{Fontname}.ttf %{buildroot}%{_fontdir}

mkdir -p %{buildroot}%{_datadir}/metainfo
install -m 0644 -p %{SOURCE2} %{buildroot}%{_datadir}/metainfo


%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/com.%{foundry}.%{fontname}.metainfo.xml


%_font_pkg %{Fontname}.ttf
%license LICENSE-BUILD
%license %{fontname}-%{version}/LICENSE
%license %{fontname}-%{version}/LICENSE-GRAPHICS
%doc %{fontname}-%{version}/CONTRIBUTING.md
%doc %{fontname}-%{version}/README.md
%{_datadir}/metainfo/com.%{foundry}.%{fontname}.metainfo.xml


%changelog
* Sat Mar 13 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 13.0.2-1
- Update to 13.0.2 (#1938403)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 13.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 13.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 17 2020 Peter Oliver <rpm@mavit.org.uk> - 13.0.1-1
- Update to version 13.0.1.

* Sat May  9 2020 Peter Oliver <rpm@mavit.org.uk> - 13.0.0-1
- Update to version 13.0.0.
- Build with noto-emoji ac1703e.

* Sat May  9 2020 Peter Oliver <rpm@mavit.org.uk> - 12.1.6-1
- Update to version 12.1.6.

* Thu Feb 13 2020 Peter Oliver <rpm@mavit.org.uk> - 12.1.5-4
- Variable vendor is reserved.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 12.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 30 2020 Peter Oliver <rpm@mavit.org.uk> - 12.1.5-2
- Build with noto-emoji 018aa14, dropping patches for Python 3.

* Wed Jan 29 2020 Peter Oliver <rpm@mavit.org.uk> - 12.1.5-1
- Update to version 12.1.5.

* Fri Nov 15 2019 Peter Oliver <rpm@mavit.org.uk> - 12.1.4-1
- Update to 12.1.4.

* Wed Oct  9 2019 Peter Oliver <rpm@mavit.org.uk> - 12.1.3-2
- Fix emojis appearing too small.

* Sat Sep 21 2019 Peter Oliver <rpm@mavit.org.uk> - 12.1.3-1
- Update to version 12.1.3

* Wed Aug 14 2019 Peter Oliver <rpm@mavit.org.uk> - 12.1.2-1
- Update to version 12.1.2.

* Tue Aug 13 2019 Peter Oliver <rpm@mavit.org.uk> - 11.3.0-3
- Build against Python 3.
- Sync build from google-noto-emoji-fonts-20190709-2.

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb  6 2019 Peter Oliver <rpm@mavit.org.uk> - 11.3.0-1
- Update to version 11.3.0.

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Peter Oliver <rpm@mavit.org.uk> - 11.2.0-1
- Update to version 11.2.0.
- Update to 2018-08-10 noto-emoji snapshot.

* Sat Aug 11 2018 Peter Oliver <rpm@mavit.org.uk> - 11.1.0-1
- Update to version 11.1.0.

* Sat Aug  4 2018 Peter Oliver <rpm@mavit.org.uk> - 11.0.1-1
- Update to version 11.0.1.
- Update URL.

* Tue Jul 31 2018 Peter Oliver <rpm@mavit.org.uk> - 11.0.0-3
- /usr/bin/python still required by noto-emoji

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun  7 2018 Peter Oliver <rpm@mavit.org.uk> - 11.0.0-1
- Update to Twemoji 11.0.0, covering Unicode 11.0.0.

* Fri May 18 2018 Peter Oliver <rpm@mavit.org.uk> - 2.7.0-1
- Update to version 2.7.0.
- Update to 2018-05-03 noto-emoji snapshot.
- Build all flags.

* Tue Apr 17 2018 Peter Oliver <rpm@mavit.org.uk> - 2.6.0-1
- Update to version 2.6.0.

* Tue Feb 20 2018 Peter Oliver <rpm@mavit.org.uk> - 2.4.0-2
- Validate metainfo.

* Wed Jan 24 2018 Peter Oliver <rpm@mavit.org.uk> - 2.4.0-1
- Update to version 2.4.0.

* Tue Dec 19 2017 Peter Oliver <rpm@mavit.org.uk> - 2.3.1-6
- Unbundle nototools.  Depends on #1527289.

* Thu Dec 14 2017 Peter Oliver <rpm@mavit.org.uk> - 2.3.1-5
- Use C.UTF-8 locale.

* Thu Dec  7 2017 Peter Oliver <rpm@mavit.org.uk> - 2.3.1-4
- Update noto-emoji.
- Pass body dimensions directly, as allowed by latest noto-emoji Makefile.

* Tue Nov 21 2017 Peter Oliver <rpm@mavit.org.uk> - 2.3.1-3
- Specify that this is an emoji font in the appstream metadata.

* Thu Nov 16 2017 Peter Oliver <rpm@mavit.org.uk> - 2.3.1-2
- Use correct image size.
- Add screenshot to AppData.

* Thu Nov 16 2017 Peter Oliver <rpm@mavit.org.uk> - 2.3.1-1
- Initial version, based on emojitwo-fonts package.
