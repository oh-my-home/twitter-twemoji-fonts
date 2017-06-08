%global commit0 86928453223b2dd8bfe8e61d70aebcae9c32f631
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global commit1 d8f3d1653f8c7c0bcc825f01d07566d122926903
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

%global fontname google-noto-emoji


Name:           google-noto-emoji-fonts
Version:        20170608
Release:        1%{?dist}
Summary:        Google Noto Emoji Fonts

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
Source2:        google-noto-emoji.metainfo.xml

Patch0:         noto-emoji-use-system-pngquant.patch

BuildArch:      noarch
BuildRequires:  fonttools
BuildRequires:  python2-fonttools
BuildRequires:  python-devel
BuildRequires:  fontpackages-devel
BuildRequires:  ImageMagick
BuildRequires:  pngquant
BuildRequires:  optipng
BuildRequires:  cairo-devel

Requires:       fontpackages-filesystem

Obsoletes:      google-noto-color-emoji-fonts < 20150617
Provides:       google-noto-color-emoji-fonts = 20150617

%description
Color and Black-and-White Noto emoji fonts, and tools for working with them.


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
install -m 0644 -p *Emoji.ttf %{buildroot}%{_fontdir}
install -m 0644 -p fonts/*.ttf %{buildroot}%{_fontdir}

mkdir -p %{buildroot}%{_datadir}/appdata
install -m 0644 -p %{SOURCE2} %{buildroot}%{_datadir}/appdata


%_font_pkg *.ttf
%license LICENSE
%doc AUTHORS CONTRIBUTING.md CONTRIBUTORS README.md
%{_datadir}/appdata/google-noto-emoji.metainfo.xml


%changelog
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
