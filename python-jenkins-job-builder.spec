%{!?_licensedir:%global license %%doc}

%if 0%{?fedora}
%global with_python3 1
%endif

%define srcname jenkins-job-builder

Name:           python-%{srcname}
Version:        2.0.0.0b1-36-ga5eb235
Release:        8%{dist}
Summary:        Manage Jenkins jobs with YAML
License:        ASL 2.0
URL:            http://ci.openstack.org/jenkins-job-builder/
Source0:        https://github.com/openstack-infra/%{srcname}/archive/2.0.0.0b1-36-ga5eb235.tar.gz
#Source0:        http://pypi.python.org/packages/source/j/%{srcname}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

%description
Jenkins Job Builder takes simple descriptions of Jenkins jobs in YAML format
and uses them to configure Jenkins. You can keep your job descriptions in
human readable text format in a version control system to make changes and
auditing easier. It also has a flexible template system, so creating many
similarly configured jobs is easy.

%package -n python2-%{srcname}
Summary:        Manage Jenkins jobs with YAML
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  pytest
BuildRequires:  python-six >= 0.3.4
BuildRequires:  python-sphinx
BuildRequires:  python-yaml
BuildRequires:  python-jenkins >= 0.3.4
BuildRequires:  python-mock
BuildRequires:  python-testtools
BuildRequires:  python-testscenarios
BuildRequires:  python-fixtures
Requires:       python-jenkins
Requires:       python-yaml
Requires:       python-pbr
Requires:       python-six >= 1.5.2
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
Jenkins Job Builder takes simple descriptions of Jenkins jobs in YAML format
and uses them to configure Jenkins. You can keep your job descriptions in
human readable text format in a version control system to make changes and
auditing easier. It also has a flexible template system, so creating many
similarly configured jobs is easy.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        Manage Jenkins jobs with YAML
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-six >= 1.5.2
BuildRequires:  python3-sphinx
BuildRequires:  python3-yaml
BuildRequires:  python3-jenkins >= 0.3.4
BuildRequires:  python3-mock
BuildRequires:  python3-testtools
BuildRequires:  python3-testscenarios
BuildRequires:  python3-fixtures
Requires:       python3-jenkins
Requires:       python3-yaml
Requires:       python3-pbr
Requires:       python3-six >= 1.5.2
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
Jenkins Job Builder takes simple descriptions of Jenkins jobs in YAML format
and uses them to configure Jenkins. You can keep your job descriptions in
human readable text format in a version control system to make changes and
auditing easier. It also has a flexible template system, so creating many
similarly configured jobs is easy.
%endif # with_python3

%prep
%autosetup -n %{srcname}-%{version} -p1

# remove shebangs
find jenkins_jobs -type f -name '*.py' \
  -exec sed -i -e '/^#!/{1D}' {} \;

# remove old Python 2.6-era requirements:
sed -i requirements.txt \
  -e '/argparse/d' \
  -e '/ordereddict/d'

# Loosen python-pbr requirement
sed -i 's/pbr>=0.8.2/pbr>=0.8.0/' requirements.txt

%build
export PBR_VERSION=%{version}

CFLAGS="-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches   -m64 -mtune=generic" %{__python2} setup.py  build --executable="%{__python2} -s"; sleep 1
# This requires sphinxcontrib-programoutput, which is not packaged in Fedora.
#make -C doc html man

%if 0%{?with_python3}
%{py3_build}
#pushd %{py3dir}
# This requires sphinxcontrib-programoutput, which is not packaged in Fedora.
#SPHINXBUILD=sphinx-build-%{python3_version} make -C doc html man
#popd
# Can't get to docs in py3dir (RHBZ #563622)
#cp -a %{py3dir}/doc py3doc
%endif # with_python3

%install

CFLAGS="-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches   -m64 -mtune=generic" %{__python2} setup.py  install -O1 --skip-build --root %{buildroot}


%if 0%{?with_python3}
  %py3_install
%endif # with_python3

%check
PYTHONPATH=%{buildroot}%{python2_sitelib} py.test-%{python2_version} -v tests

%if 0%{?with_python3}
  PYTHONPATH=%{buildroot}%{python3_sitelib} py.test-%{python3_version} -v tests
%endif # with_python3

%files -n python2-%{srcname}
%license LICENSE
#doc doc/build/html
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-%{srcname}
%license LICENSE
#doc doc/build/html
%{python3_sitelib}/*
%endif # with_python3

# Will go to python3 subpkg when enabled, otherwise to python2
%{_bindir}/jenkins-jobs

%changelog
* Tue Mar 7 2017 Matthieu Huin <mhuin@redhat.com> - 2.0.0.0b1-36-ga5eb235-8
- Rebuild for Software Factory

* Wed Oct 19 2016 brian@bstinson.com 1.6.1-7.centos
- Rebuild for the latest version for use in ci.centos.org

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Apr 06 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.4.0-6
- Backport patch to fix py3 version

* Tue Apr 05 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.4.0-5
- Use more python2- prefixed package in requires
- Simplify providing binary of jenkins-jobs

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Paul Belanger <pabelanger@redhat.com> - 1.4.0-3
- Add Requires python-six (rhbz#1298324)

* Thu Jan 07 2016 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.4.0-2
- Drop another Fedora 20 conditional (and implicitly add RHEL 7 support)
- Drop unneeded %%python_sitelib definition

* Tue Dec 29 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.4.0-1
- update to 1.4.0 (rhbz#1294527)

* Fri Dec 04 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.3.0-5
- Fix Requires on py2/py3 subpackages

* Thu Dec 03 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.3.0-4
- Patch to fix mavenName XML sorting on py35
- Make tests fail the build for py3
- Drop Fedora 20 conditionals

* Sat Nov 14 2015 Ken Dreyer <ktdreyer@ktdreyer.com>
- Fix FTBFS with Python 3.5
- Run tests on python3 (still fail due to mavenName XML sorting issue)
- rm Group tag
- Rename Python 2 subpackage to "python2-"
- Update for latest Python packaging guidelines
- Switch /usr/bin/jenkins-jobs to Python 3 on Fedora 24 and newer

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Aug 27 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.3.0-1
- update to 1.3.0 (rhbz#1257377)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.2.0-1
- update to 1.2.0 (rhbz#1222209)

* Fri Apr 03 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.0-1
- update to 1.1.0
- rm python3_version compat macro; this has been defined since F13
- remove hard-coded srcname in some places
- add more test suite BRs
- run tests using py.test directly instead of setuptools
- add LICENSE

* Wed Nov 19 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.0-1
- update to 1.0.0
- rm argparse dep (this is in Python 2.7 core)
- Use PBR_VERSION instead of trying to avoid pbr.

* Wed Nov 19 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.9.0-0.20141111gitgbaff62b.1
- update to post-release git snapshot

* Tue Nov 11 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.9.0-1
- New package.
