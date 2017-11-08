%global commit0 411334c8e630acf858569602cbf5c19deba00878
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global commit1 0c99dfff2a824c6f7210ff700c56b2c3d51e64cd
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

%global fontname google-noto-emoji


Name:           %{fontname}-fonts
Version:        20170928
Release:        2%{?dist}
Summary:        Google “Noto Emoji” Black-and-White emoji font

# In noto-emoji-fonts source
## noto-emoji code is in ASL 2.0 license
## Emoji fonts are under OFL license
### third_party color-emoji code is in BSD license
### third_party region-flags code is in Public Domain license
# In nototools source
## nototools code is in ASL 2.0 license
### third_party ucd code is in Unicode license
License:        OFL and ASL 2.0
URL:            https://github.com/googlei18n/noto-emoji
Source0:        https://github.com/googlei18n/noto-emoji/archive/%{commit0}.tar.gz#/noto-emoji-%{shortcommit0}.tar.gz
Source1:        https://github.com/googlei18n/nototools/archive/%{commit1}.tar.gz#/nototools-%{shortcommit1}.tar.gz
Source2:        %{fontname}.metainfo.xml
Source3:        %{fontname}-color.metainfo.xml

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

Obsoletes:      google-noto-color-emoji-fonts < 20150617
Provides:       google-noto-color-emoji-fonts = 20150617

%description
This package provides the Google “Noto Emoji” Black-and-White emoji font.

%package -n     %{fontname}-color-fonts
Summary:        Google “Noto Color Emoji” colored emoji font
Requires:       fontpackages-filesystem
Obsoletes:      google-noto-color-emoji-fonts < 20150617
Provides:       google-noto-color-emoji-fonts = 20150617

%description -n %{fontname}-color-fonts
This package provides the Google “Noto Color Emoji” colored emoji font.

%prep
%autosetup -n noto-emoji-%{commit0}

rm -rf third_party/pngquant
tar zxf %{SOURCE1}
rm -rf nototools-%{commit1}/third_party/{cldr,dspl,fontcrunch,ohchr,spiro,udhr,unicode}

%build
# Work around UTF-8
export LANG=zh_CN.UTF-8

pushd nototools-%{commit1}
export PATH=$PATH:"$PWD/nototools"
export PYTHONPATH=$PWD
popd

make %{?_smp_mflags} OPT_CFLAGS="$RPM_OPT_FLAGS"

%install
install -m 0755 -d %{buildroot}%{_fontdir}

# Built by us from the supplied pngs:
install -m 0644 -p NotoColorEmoji.ttf %{buildroot}%{_fontdir}

# Pre-built, and included with the source:
install -m 0644 -p fonts/NotoEmoji-Regular.ttf %{buildroot}%{_fontdir}

mkdir -p %{buildroot}%{_datadir}/appdata
install -m 0644 -p %{SOURCE2} %{buildroot}%{_datadir}/appdata
install -m 0644 -p %{SOURCE3} %{buildroot}%{_datadir}/appdata

%_font_pkg NotoEmoji-Regular.ttf
%license LICENSE
%doc AUTHORS CONTRIBUTING.md CONTRIBUTORS README.md
%{_datadir}/appdata/google-noto-emoji.metainfo.xml

%_font_pkg -n color NotoColorEmoji.ttf
%license LICENSE
%doc AUTHORS CONTRIBUTING.md CONTRIBUTORS README.md
%{_datadir}/appdata/google-noto-emoji-color.metainfo.xml


%changelog
* Wed Nov  8 2017 Peter Oliver <rpm@mavit.org.uk> - 20170928-2
- Prefer zopflipng to optipng, since it should yield smaller files.
- Use the font we built, rather than the one included with the source.

* Thu Sep 28 2017 Mike FABIAN <mfabian@redhat.com> - 20170828-1
- Update to upstream snapshot tarball
- split black-and-white and color fonts into different sub-packages.

* Mon Aug 28 2017 Mike FABIAN <mfabian@redhat.com> - 20170827-1
- Update to upstream snapshot tarball
- Update color emoji font to version 2.001, new design.
- Contains the new emoji added in Unicode 10.0.0.

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170608-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 08 2017 Mike FABIAN <mfabian@redhat.com> - 20170608-1
- Update to upstream snapshot tarball

* Tue May 23 2017 Mike FABIAN <mfabian@redhat.com> - 20170523-1
- Update to upstream snapshot tarball
- This fixes the skin tones of the light/medium light male cook emoji,
  which had been swapped.

* Wed Apr 26 2017 Mike FABIAN <mfabian@redhat.com> - 20170426-1
- Update to upstream snapshot tarball
  (fixes the family emoji sequences:
  kiss: woman, man U+1F469 U+200D U+2764 U+FE0F U+200D U+1F48B U+200D U+1F468
  couple with heart: woman, man U+1F469 U+200D U+2764 U+FE0F U+200D U+1F468)

* Thu Feb 23 2017 Peng Wu <pwu@redhat.com> - 20170223-1
- Update to upstream snapshot tarball

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20160406-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri May  6 2016 Peng Wu <pwu@redhat.com> - 20160406-5
- Avoid to use python setup.py

* Fri Apr 29 2016 Peng Wu <pwu@redhat.com> - 20160406-4
- Replace google-noto-color-emoji-fonts package

* Mon Apr 25 2016 Peng Wu <pwu@redhat.com> - 20160406-3
- Add google-noto-emoji.metainfo.xml

* Wed Apr 20 2016 Peng Wu <pwu@redhat.com> - 20160406-2
- Use system pngquant

* Wed Apr 20 2016 Peng Wu <pwu@redhat.com> - 20160406-1
- Initial packaging
