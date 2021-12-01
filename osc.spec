#
# spec file for package osc
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%if 0%{?suse_version} >= 1500 || 0%{?fedora_version} >= 29 || 0%{?centos_version} >= 800 || 0%{?mageia} >= 8
%bcond_without python3
%else
%bcond_with    python3
%endif
%if %{with python3}
%define use_python python3
%else
%define use_python python
%endif

%define version_unconverted 0.174.0
%define osc_plugin_dir %{_prefix}/lib/osc-plugins
%define macros_file macros.osc
%if ! %{defined _rpmmacrodir}
 %define _rpmmacrodir %{_sysconfdir}/rpm
%endif

Name:           osc
Version:        0.174.0
Release:        0
Summary:        Open Build Service Commander
License:        GPL-2.0-or-later
Group:          Development/Tools/Other
URL:            https://github.com/openSUSE/osc
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  %{use_python}-devel
BuildRequires:  %{use_python}-setuptools
BuildRequires:  diffstat
%if 0%{?mandriva_version} || 0%{?mageia}
BuildRequires:  python-rpm
Requires:       python-rpm
%else
%if 0%{?suse_version} >= 1500 || 0%{?fedora_version} >= 32 || 0%{?centos_version} >= 800
BuildRequires:  %{use_python}-rpm
Requires:       %{use_python}-rpm
%else
BuildRequires:  rpm-python
Requires:       rpm-python
%endif
%endif
%if 0%{?suse_version} == 0 || 0%{?suse_version} >= 1120
BuildArch:      noarch
%endif
%if 0%{?suse_version}
Requires:       %{use_python}
Recommends:     %{use_python}-progressbar
BuildRequires:  %{use_python}-xml
Requires:       %{use_python}-xml
%if !%{with python3} && 0%{?suse_version} < 1020
BuildRequires:  python-elementtree
Requires:       python-elementtree
%endif
%if 0%{?suse_version} > 1000
Recommends:     build
Recommends:     ca-certificates
Recommends:     diffstat
Recommends:     obs-git
Recommends:     powerpc32
Recommends:     sudo
# These packages are needed for "osc add $URL"
Recommends:     obs-service-recompress
Recommends:     obs-service-download_files
Recommends:     obs-service-format_spec_file
Recommends:     obs-service-obs_scm
Recommends:     obs-service-set_version
Recommends:     obs-service-source_validator
Recommends:     obs-service-tar_scm
Recommends:     obs-service-verify_file
Recommends:     xdg-utils
# for osc >= 0.167.0 the newest build version is needed.
# Otherwise osc chroot might not work correctly.
Conflicts:      build < 20200106
%endif
%endif
# needed for storing credentials in kwallet/gnome-keyring
%if 0%{?suse_version} > 1000 || 0%{?mandriva_version} || 0%{?mdkversion}
%if %{with python3}
Recommends:     python3-keyring
%else
Recommends:     python-keyring
%endif
%endif
%if 0%{?rhel_version} && 0%{?rhel_version} < 600
BuildRequires:  python-elementtree
Requires:       python-elementtree
%endif
%if 0%{?centos_version} && 0%{?centos_version} < 600
BuildRequires:  python-elementtree
Requires:       python-elementtree
%endif
%if 0%{?suse_version} || 0%{?mandriva_version} || 0%{?mageia}
%if 0%{?suse_version} >= 1500
BuildRequires:  %{use_python}-M2Crypto > 0.19
BuildRequires:  %{use_python}-chardet
Requires:       %{use_python}-M2Crypto > 0.19
Requires:       %{use_python}-chardet
%else
BuildRequires:  python-m2crypto > 0.19
Requires:       python-m2crypto > 0.19
%endif
%else
%if 0%{?fedora_version} >= 29  || 0%{?centos_version} >= 800
BuildRequires:  python3-m2crypto
Requires:       python3-m2crypto
%else
BuildRequires:  m2crypto > 0.19
Requires:       m2crypto > 0.19
%endif
%endif

Provides:       %{use_python}-osc

%if %{with python3}
%define python_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%else
%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

%description
Commandline client for the Open Build Service.

See http://en.opensuse.org/openSUSE:OSC , as well as
http://en.opensuse.org/openSUSE:Build_Service_Tutorial for a general
introduction.

%prep
%setup -q -D -T 0 -n %_sourcedir

%build
# the PATH hack/rewrite is needed for Fedora 20 builds, because /bin
# is a symlink to /usr/bin and /bin precedes /usr/bin in PATH
# => a "wrong" interpreter line ("#!/bin/python") is constructed
# ("wrong", because no package provides "/bin/python").
PATH="/usr/bin:$PATH" CFLAGS="%{optflags}" %{use_python} setup.py build

cat << eom > %{macros_file}
%%osc_plugin_dir %{osc_plugin_dir}
eom
echo >> %{macros_file}

%install
%{use_python} setup.py install --prefix=%{_prefix} --root=%{buildroot}
perl -p -i -e 's{#!.*python}{#!%{_bindir}/%{use_python}}' osc-wrapper.py
ln -s osc-wrapper.py %{buildroot}/%{_bindir}/osc
mkdir -p %{buildroot}%{osc_plugin_dir}
mkdir -p %{buildroot}%{_localstatedir}/lib/osc-plugins
install -Dm0644 dist/complete.csh %{buildroot}%{_sysconfdir}/profile.d/osc.csh
%if 0%{?suse_version}
install -Dm0644 dist/complete.sh %{buildroot}%{_sysconfdir}/bash_completion.d/osc.sh
%else
install -Dm0644 dist/complete.sh %{buildroot}%{_sysconfdir}/profile.d/osc.sh
%endif
%if 0%{?suse_version} > 1110
install -Dm0755 dist/osc.complete %{buildroot}%{_prefix}/lib/osc/complete
%else
install -Dm0755 dist/osc.complete %{buildroot}%{_libdir}/osc/complete
%endif

install -Dm644 osc.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/osc.fish

install -m644 %{macros_file} -D %{buildroot}%{_rpmmacrodir}/%{macros_file}

%if 0%{?suse_version} >= 1500
%check
exit 0
cd tests
%{use_python} suite.py
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%if 0%{?suse_version} >= 1500
%license COPYING
%doc AUTHORS README TODO NEWS
%else
%doc AUTHORS README TODO NEWS COPYING
%endif
%{_bindir}/osc*
%{python_sitelib}/*
%config %{_sysconfdir}/profile.d/osc.csh
%if 0%{?suse_version}
%config %{_sysconfdir}/bash_completion.d/osc.sh
%else
%config %{_sysconfdir}/profile.d/osc.sh
%endif
%{_rpmmacrodir}/%{macros_file}
%dir %{_localstatedir}/lib/osc-plugins
%{_mandir}/man1/osc.*
%if 0%{?suse_version} > 1110
%{_prefix}/lib/osc
%else
%{_libdir}/osc
%endif
%dir %{_datadir}/fish
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/osc.fish
%dir %{osc_plugin_dir}

%changelog
