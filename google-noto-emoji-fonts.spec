%global commit0 e7a7241a929625feb16920a40bfa29e4a302b82b
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global commit1 c1f2cffbba35d08c9558006bc7860492ce322b87
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

%global fontname google-noto-emoji


Name:           google-noto-emoji-fonts
Version:        20160406
Release:        3%{?dist}
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
BuildRequires:  python2-fonttools
BuildRequires:  python-devel
BuildRequires:  fontpackages-devel
BuildRequires:  ImageMagick
BuildRequires:  pngquant
BuildRequires:  optipng
BuildRequires:  cairo-devel

Requires:       fontpackages-filesystem

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
%{__python2} setup.py develop --user
popd

export PATH=$PATH:$HOME/.local/bin

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
* Mon Apr 25 2016 Peng Wu <pwu@redhat.com> - 20160406-3
- Add google-noto-emoji.metainfo.xml

* Wed Apr 20 2016 Peng Wu <pwu@redhat.com> - 20160406-2
- Use system pngquant

* Wed Apr 20 2016 Peng Wu <pwu@redhat.com> - 20160406-1
- Initial packaging
