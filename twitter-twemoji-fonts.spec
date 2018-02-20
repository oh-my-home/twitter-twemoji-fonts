%global commit0 411334c8e630acf858569602cbf5c19deba00878
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global vendor twitter
%global fontname twemoji
%global Fontname Twemoji


Name:           %{vendor}-%{fontname}-fonts
Version:        2.4.0
Release:        2%{?dist}
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
URL:            https://twitter.github.io/twemoji
Source0:        https://github.com/googlei18n/noto-emoji/archive/%{commit0}.tar.gz#/noto-emoji-%{shortcommit0}.tar.gz
Source2:        com.%{vendor}.%{fontname}.metainfo.xml
Source4:        https://github.com/%{vendor}/%{fontname}/archive/v%{version}.tar.gz#/%{fontname}-%{version}.tar.gz

Patch0:         noto-emoji-use-system-pngquant.patch

BuildArch:      noarch
BuildRequires:  ImageMagick
BuildRequires:  cairo-devel
BuildRequires:  fontpackages-devel
BuildRequires:  fonttools
BuildRequires:  libappstream-glib
BuildRequires:  nototools
BuildRequires:  pngquant
BuildRequires:  python2-devel
BuildRequires:  python2dist(fonttools)
BuildRequires:  zopfli

Requires:       fontpackages-filesystem


%description
A color emoji font with a flat visual style, designed and used by Twitter.


%prep
%autosetup -n noto-emoji-%{commit0}
rm -rf third_party/pngquant
mv LICENSE LICENSE-BUILD

tar -xf %{SOURCE4}
sed 's/Noto Color Emoji/Twemoji/; s/NotoColorEmoji/Twemoji/; s/Copyright .* Google Inc\./Twitter, Inc and other contributors./; s/ Version .*/ %{version}/; s/.*is a trademark.*//; s/Google, Inc\./Twitter, Inc and other contributors/; s,http://www.google.com/get/noto/,https://github.com/twitter/twemoji/,; s/.*is licensed under.*/      Creative Commons Attribution 4.0 International/; s,http://scripts.sil.org/OFL,http://creativecommons.org/licenses/by/4.0/,' NotoColorEmoji.tmpl.ttx.tmpl > Twemoji.tmpl.ttx.tmpl
pushd %{fontname}-%{version}/2/72x72/
for png in *.png; do
    mv $png emoji_u${png//-/_}
done
popd


%build
# Prevent python 2 crash in Koji when outputting Unicode characters:
export LANG=C.UTF-8

make %{?_smp_mflags} OPT_CFLAGS="$RPM_OPT_FLAGS" EMOJI=%{Fontname} EMOJI_SRC_DIR=%{fontname}-%{version}/2/72x72 FLAGS= BODY_DIMENSIONS=76x72


%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p %{Fontname}.ttf %{buildroot}%{_fontdir}

mkdir -p %{buildroot}%{_datadir}/metainfo
install -m 0644 -p %{SOURCE2} %{buildroot}%{_datadir}/metainfo


%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/%{fontname}.metainfo.xml


%_font_pkg %{Fontname}.ttf
%license LICENSE-BUILD
%license %{fontname}-%{version}/LICENSE
%license %{fontname}-%{version}/LICENSE-GRAPHICS
%doc %{fontname}-%{version}/CONTRIBUTING.md
%doc %{fontname}-%{version}/README.md
%{_datadir}/metainfo/com.%{vendor}.%{fontname}.metainfo.xml


%changelog
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
