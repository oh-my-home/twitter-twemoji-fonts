%global commit0 411334c8e630acf858569602cbf5c19deba00878
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global commit1 0c99dfff2a824c6f7210ff700c56b2c3d51e64cd
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

%global vendor twitter
%global fontname twemoji
%global Fontname Twemoji


Name:           %{vendor}-%{fontname}-fonts
Version:        2.3.1
Release:        3%{?dist}
Summary:        Twitter Emoji for everyone

# In noto-emoji-fonts source
## noto-emoji code is in ASL 2.0 license
## Emoji fonts are under OFL license
### third_party color-emoji code is in BSD license
### third_party region-flags code is in Public Domain license
# In nototools source
## nototools code is in ASL 2.0 license
### third_party ucd code is in Unicode license
# In twemoji source
## Artwork is Creative Commons Attribution 4.0 International
## Non-artwork is MIT
License:        OFL and ASL 2.0 and CC-BY and MIT
URL:            https://twitter.github.io/twemoji
Source0:        https://github.com/googlei18n/noto-emoji/archive/%{commit0}.tar.gz#/noto-emoji-%{shortcommit0}.tar.gz
Source1:        https://github.com/googlei18n/nototools/archive/%{commit1}.tar.gz#/nototools-%{shortcommit1}.tar.gz
Source2:        com.%{vendor}.%{fontname}.metainfo.xml
Source4:        https://github.com/%{vendor}/%{fontname}/archive/v%{version}.tar.gz#/%{fontname}-%{version}.tar.gz

Patch0:         noto-emoji-use-system-pngquant.patch

BuildArch:      noarch
BuildRequires:  fonttools
BuildRequires:  python2-fonttools
BuildRequires:  python-devel
BuildRequires:  fontpackages-devel
BuildRequires:  ImageMagick
BuildRequires:  pngquant
BuildRequires:  zopfli
BuildRequires:  cairo-devel

Requires:       fontpackages-filesystem


%description
A color emoji font with a flat visual style, designed and used by Twitter.


%prep
%autosetup -n noto-emoji-%{commit0}
rm -rf third_party/pngquant
mv LICENSE LICENSE-BUILD

tar -xf %{SOURCE1}
rm -rf nototools-%{commit1}/third_party/{cldr,dspl,fontcrunch,ohchr,spiro,udhr,unicode}

tar -xf %{SOURCE4}
sed 's/Noto Color Emoji/Twemoji/; s/NotoColorEmoji/Twemoji/; s/Copyright .* Google Inc\./Twitter, Inc and other contributors./; s/ Version .*/ %{version}/; s/.*is a trademark.*//; s/Google, Inc\./Twitter, Inc and other contributors/; s,http://www.google.com/get/noto/,https://github.com/twitter/twemoji/,; s/.*is licensed under.*/      Creative Commons Attribution 4.0 International/; s,http://scripts.sil.org/OFL,http://creativecommons.org/licenses/by/4.0/,' NotoColorEmoji.tmpl.ttx.tmpl > Twemoji.tmpl.ttx.tmpl
pushd %{fontname}-%{version}/2/72x72/
for png in *.png; do
    mv $png emoji_u${png//-/_}
done
popd


%build
# Work around UTF-8
export LANG=zh_CN.UTF-8

pushd nototools-%{commit1}
export PATH=$PATH:"$PWD/nototools"
export PYTHONPATH=$PWD
popd

make %{?_smp_mflags} OPT_CFLAGS="$RPM_OPT_FLAGS" EMOJI=%{Fontname} EMOJI_SRC_DIR=%{fontname}-%{version}/2/72x72 FLAGS= IMOPS=" -size 76x72 canvas:none -compose copy -gravity center"


%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p %{Fontname}.ttf %{buildroot}%{_fontdir}

mkdir -p %{buildroot}%{_datadir}/appdata
install -m 0644 -p %{SOURCE2} %{buildroot}%{_datadir}/appdata

%_font_pkg %{Fontname}.ttf
%license LICENSE-BUILD
%license %{fontname}-%{version}/LICENSE
%license %{fontname}-%{version}/LICENSE-GRAPHICS
%doc %{fontname}-%{version}/CONTRIBUTING.md
%doc %{fontname}-%{version}/README.md
%{_datadir}/appdata/com.%{vendor}.%{fontname}.metainfo.xml


%changelog
* Tue Nov 21 2017 Peter Oliver <rpm@mavit.org.uk> - 2.3.1-3
- Specify that this is an emoji font in the appstream metadata.

* Thu Nov 16 2017 Peter Oliver <rpm@mavit.org.uk> - 2.3.1-2
- Use correct image size.
- Add screenshot to AppData.

* Thu Nov 16 2017 Peter Oliver <rpm@mavit.org.uk> - 2.3.1-1
- Initial version, based on emojitwo-fonts package.
