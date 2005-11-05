Summary:	Linux Video Editor
Summary(pl):	Linux Video Editor - edytor filmów dla Linuksa
Name:		lve
%define _snap 050112
Version:	0.%{_snap}
Release:	0.1
License:	GPL
Group:		Applications/Multimedia
URL:		http://lvempeg.sourceforge.net/
Source0:	http://dl.sourceforge.net/lvempeg/%{name}-%{_snap}.src.tar.bz2
# Source0-md5:	0752ec29e7fe2fa1be83d9a86441b3bb
Source1:	http://dl.sourceforge.net/ffmpeg/ffmpeg-0.4.8.tar.gz
# Source1-md5:	e00d47614ba1afd99ad2ea387e782dd9
Patch0:		%{name}-a52dec.patch
Patch1:		%{name}-path.patch
Patch2:		%{name}-optflags.patch
BuildRequires:	SDL-devel
BuildRequires:	XFree86-devel
BuildRequires:	a52dec-libs-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	gcc-c++ >= 5:3.3.0
BuildRequires:	mpeg2dec-devel
BuildRequires:	qt-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LVE provides frame and GOP accurate editing of MPEG1/2 elementary
("ES") and program streams ("PS"), including VOB format. The cutting
engine is based on a frame server (demuxer), which guarantees exact
and fast seeking to every frame. The GUI is based on libSDL. Video
scenes are handled as thumbnails movable by drag and drop. Final
videos can be build with or without re-encoding. Tools for shrinking
and DVD authoring are also available.

%description -l pl
LVE pozwala na edycjê z dok³adno¶ci± do klatki i GOP strumieni
elementarnych ("ES") oraz programowych ("PS") MPEG1/2, w³±cznie z
formatem VOB. Silnik obcinaj±cy jest oparty na serwerze ramek
(demuxerze), gwarantuj±cym dok³adne i szybkie przeskakiwanie do ka¿dej
klatki. Interfejs graficzny oparty jest na libSDL. Sceny filmów mo¿na
tworzyæ z lub bez ponownego kodowania. Dostêpne s± tak¿e narzêdzia do
zmniejszania i sk³adania DVD.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1

#sed -i "s,liba52/,a52dec/,g" src/*
tar -xzf %{SOURCE1}
ln -snf ffmpeg-0.4.8 ffmpeg

rm -rf mpeg2dec{,-0.4.0}

ln -sf global_config.gcc330 src/global_config

%build
%{__make} -C qdir \
	CC="%{__cxx}" \
	CFLAGS="%{rpmcxxflags}" \
	QT_INCLUDE=-I%{_includedir}/qt

%{__make} all-recursive \
	CC="%{__cxx}" \
	OPTFLAGS="%{rpmcxxflags}" \
	INCLUDE="-I../ffmpeg/libavcodec -I%{_includedir}/mpeg2dec" \
	QT_DIR=%{_prefix} \
	SUBDIRS="src"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/lve/lib
install lib/* $RPM_BUILD_ROOT%{_datadir}/lve/lib
install -D src/lve $RPM_BUILD_ROOT%{_bindir}/lve
install -D src/lvedemux $RPM_BUILD_ROOT%{_bindir}/lvedemux
install -D src/lvedump $RPM_BUILD_ROOT%{_bindir}/lvedump
install -D src/lvemkdvd $RPM_BUILD_ROOT%{_bindir}/lvemkdvd
install -D src/lvemkidx $RPM_BUILD_ROOT%{_bindir}/lvemkidx
install -D src/lvemux $RPM_BUILD_ROOT%{_bindir}/lvemux
install -D src/lverequant $RPM_BUILD_ROOT%{_bindir}/lverequant
install -D qdir/qdir $RPM_BUILD_ROOT%{_bindir}/qdir
install -D bin/lvefilter $RPM_BUILD_ROOT%{_bindir}/lvefilter

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog COPYING DVD-Authoring.txt Readme.avsync Readme.lvemux
%attr(755,root,root) %{_bindir}/*
%{_datadir}/lve
