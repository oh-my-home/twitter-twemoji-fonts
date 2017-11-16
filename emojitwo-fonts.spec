%global commit0 411334c8e630acf858569602cbf5c19deba00878
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global commit1 0c99dfff2a824c6f7210ff700c56b2c3d51e64cd
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

%global commit4 0c1652165f02af6f42e0d4a44cd52c4f1098b8f4
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})

%global fontname emojitwo


Name:           %{fontname}-fonts
Version:        20171019git%{shortcommit4}
Release:        2%{?dist}
Summary:        Color emoji font with a flat style

# In noto-emoji-fonts source
## noto-emoji code is in ASL 2.0 license
## Emoji fonts are under OFL license
### third_party color-emoji code is in BSD license
### third_party region-flags code is in Public Domain license
# In nototools source
## nototools code is in ASL 2.0 license
### third_party ucd code is in Unicode license
# In emojitwo source
## Artwork is Creative Commons Attribution 4.0 International
## Non-artwork is MIT
License:        OFL and ASL 2.0 and CC-BY and MIT
URL:            https://emojitwo.github.io/
Source0:        https://github.com/googlei18n/noto-emoji/archive/%{commit0}.tar.gz#/noto-emoji-%{shortcommit0}.tar.gz
Source1:        https://github.com/googlei18n/nototools/archive/%{commit1}.tar.gz#/nototools-%{shortcommit1}.tar.gz
Source2:        %{fontname}.metainfo.xml
Source4:        https://github.com/EmojiTwo/emojitwo/archive/%{commit4}.tar.gz#/emojitwo-%{shortcommit4}.tar.gz

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
Maintained fork of the last fully free version of Ranks.com's Emoji One font.


%prep
%autosetup -n noto-emoji-%{commit0}
rm -rf third_party/pngquant

tar -xf %{SOURCE1}
rm -rf nototools-%{commit1}/third_party/{cldr,dspl,fontcrunch,ohchr,spiro,udhr,unicode}

tar -xf %{SOURCE4}
sed 's/Noto Color Emoji/Emoji Two/; s/Noto Color Emoji/EmojiTwo/; s/Copyright .* Google Inc\./Ranks.com with contributions from the EmojiTwo community./; s/ Version .*/ %{version}/; s/.*is a trademark.*/      Emoji One is a trademark of Ranks.com./; s/Google, Inc\./Ranks.com and the EmojiTwo community/; s,http://www.google.com/get/noto/,https://emojitwo.github.io/,; s/.*is licensed under.*/      Creative Commons Attribution 4.0 International/; s,http://scripts.sil.org/OFL,http://creativecommons.org/licenses/by/4.0/,' NotoColorEmoji.tmpl.ttx.tmpl > EmojiTwo.tmpl.ttx.tmpl
pushd emojitwo-%{commit4}/png/128/
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

make %{?_smp_mflags} OPT_CFLAGS="$RPM_OPT_FLAGS" EMOJI=EmojiTwo EMOJI_SRC_DIR=emojitwo-%{commit4}/png/128 FLAGS=


%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p EmojiTwo.ttf %{buildroot}%{_fontdir}

mkdir -p %{buildroot}%{_datadir}/appdata
install -m 0644 -p %{SOURCE2} %{buildroot}%{_datadir}/appdata

%_font_pkg EmojiTwo.ttf
%license LICENSE emojitwo-%{commit4}/LICENSE.md
%doc emojitwo-%{commit4}/CONTRIBUTING.md emojitwo-%{commit4}/README.md
%{_datadir}/appdata/emojitwo.metainfo.xml


%changelog
* Thu Nov 16 2017 Peter Oliver <rpm@mavit.org.uk> - 20171019git0c16521-2
- Add a screenshot to the AppData.

* Thu Nov  9 2017 Peter Oliver <rpm@mavit.org.uk> - 20171019git0c16521-1
- Initial version, based on google-noto-emoji-fonts package.
