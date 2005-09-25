Summary:	Linux Video Editor
Name:		lve
%define _snap 040322
Version:	0.%{_snap}
Release:	1
License:	GPL
Group:		Applications/Multimedia
URL:		http://lvempeg.sourceforge.net/
Source0:	http://dl.sourceforge.net/lvempeg/%{name}-%{_snap}.src.tar.bz2
# Source0-md5:	079f976cee2b26a96caf3e4428c6456d
Source1:	http://dl.sourceforge.net/ffmpeg/ffmpeg-0.4.8.tar.gz
# Source1-md5:	e00d47614ba1afd99ad2ea387e782dd9
BuildRequires:	SDL-devel
BuildRequires:	XFree86-devel
BuildRequires:	a52dec-libs-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	gcc-c++
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

%prep
%setup -q -n %{name}

sed -i "s,liba52/,a52dec/,g" src/*
tar -xzvf %{SOURCE1}
rm ffmpeg
ln -s ffmpeg-0.4.8 ffmpeg
sed -i "s,%{_prefix}/local/lve/bin/lverequant,%{_bindir}/lverequant,g" src/lvedump.c
sed -i "s,%{_prefix}/local/lve/lib,%{_datadir}/lve/lib,g" src/lve.h
sed -i "s,%{_prefix}/local/lve/bin,%{_bindir},g" src/lve.h

%build
%{__make} -C qdir \
	QT_INCLUDE=-I%{_includedir}/qt

%{__make} all-recursive \
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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog COPYING DVD-Authoring.txt Readme.avsync Readme.lvemux
%attr(755,root,root) %{_bindir}/*
%{_datadir}/lve
