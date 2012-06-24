# $Id: lve.spec,v 1.1 2005-09-25 11:37:49 glen Exp $
# Authority: dries

%define real_version 040322

Summary: Linux Video Editor
Name: lve
Version: 0.%{real_version}
Release: 1
License: GPL
Group: Applications/Multimedia
URL: http://lvempeg.sourceforge.net/

Packager: Dries Verachtert <dries@ulyssis.org>
Vendor: Dries Apt/Yum Repository http://dries.ulyssis.org/ayo/

Source: http://dl.sf.net/lvempeg/lve-%{real_version}.src.tar.bz2
Source1: http://dl.sf.net/ffmpeg/ffmpeg-0.4.8.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: ffmpeg-devel, mpeg2dec-devel, SDL-devel, gcc-c++, qt-devel
BuildRequires: XFree86-devel, a52dec-devel

%description
LVE provides frame and GOP accurate editing of MPEG1/2 elementary ("ES") and
program streams ("PS"), including VOB format. The cutting engine is based on
a frame server (demuxer), which guarantees exact and fast seeking to every
frame. The GUI is based on libSDL. Video scenes are handled as thumbnails
movable by drag and drop. Final videos can be build with or without
re-encoding. Tools for shrinking and DVD authoring are also available. 

%prep
%setup -n lve

%build
# fix permissions of devel dir
%{__chmod} -R u+w .
. /etc/profile.d/qt.sh
sed -i "s/liba52\//a52dec\//g;" src/*
%{__tar} -xzvf %{SOURCE1}
%{__rm} ffmpeg
ln -s ffmpeg-0.4.8 ffmpeg
sed -i "s/\/usr\/local\/lve\/bin\/lverequant/\/usr\/bin\/lverequant/g;" src/lvedump.c
sed -i "s/\/usr\/local\/lve\/lib/\/usr\/share\/lve\/lib/g;" src/lve.h
sed -i "s/\/usr\/local\/lve\/bin/\/usr\/bin/g;" src/lve.h
%{__make} all-recursive INCLUDE="-I../ffmpeg/libavcodec -I/usr/include/mpeg2dec" QT_DIR=${QTDIR} SUBDIRS="qdir src" %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__install} -d -m755 %{buildroot}%{_datadir}/lve/lib
%{__install} -m755 lib/* %{buildroot}%{_datadir}/lve/lib/
%{__install} -m755 -D src/lve %{buildroot}%{_bindir}/lve
%{__install} -m755 -D src/lvedemux %{buildroot}%{_bindir}/lvedemux
%{__install} -m755 -D src/lvedump %{buildroot}%{_bindir}/lvedump
%{__install} -m755 -D src/lvemkdvd %{buildroot}%{_bindir}/lvemkdvd
%{__install} -m755 -D src/lvemkidx %{buildroot}%{_bindir}/lvemkidx
%{__install} -m755 -D src/lvemux %{buildroot}%{_bindir}/lvemux
%{__install} -m755 -D src/lverequant %{buildroot}%{_bindir}/lverequant
%{__install} -m755 -D qdir/qdir %{buildroot}%{_bindir}/qdir
%{__install} -m755 -D bin/lvefilter %{buildroot}%{_bindir}/lvefilter

%post
/sbin/ldconfig 2>/dev/null

%postun
/sbin/ldconfig 2>/dev/null

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc ChangeLog COPYING DVD-Authoring.txt Readme.avsync Readme.lvemux
%{_bindir}/*
%{_datadir}/lve/

%changelog
$Log: lve.spec,v $
Revision 1.1  2005-09-25 11:37:49  glen
- initial import from http://dag.wieers.com/packages/lve/lve.spec

* Tue Jun 1 2004 Dries Verachtert <dries@ulyssis.org> - 0.040322-1
- Initial package.
