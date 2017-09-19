%{?scl:%scl_package eclipse-dltk}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 1

%global gittag R5_7_1

Name:      %{?scl_prefix}eclipse-dltk
Version:   5.7.1
Release:   1.%{baserelease}%{?dist}
Summary:   Dynamic Languages Toolkit (DLTK) Eclipse plug-in
License:   EPL and (CPL or GPLv2+ or LGPLv2+) and Ruby and ASL 2.0
URL:       http://www.eclipse.org/dltk/

# source tarball and the script used to generate it from upstream's source control
# script usage:
# $ sh get-dltk.sh
Source0:   eclipse-dltk-%{gittag}.tar.xz
Source1:   get-dltk.sh

# Port to latest system lucene
Patch0:    eclipse-dltk-lucene.patch

BuildArch:        noarch

BuildRequires:    %{?scl_prefix}eclipse-license >= 1.0.1
BuildRequires:    %{?scl_prefix}eclipse-pde >= 1:4.6.0
BuildRequires:    %{?scl_prefix}eclipse-emf-runtime
BuildRequires:    %{?scl_prefix}eclipse-mylyn >= 3.21.0-4
BuildRequires:    %{?scl_prefix}eclipse-rse
BuildRequires:    %{?scl_prefix}eclipse-manpage
BuildRequires:    %{?scl_prefix}h2
BuildRequires:    %{?scl_prefix_java_common}lucene5
BuildRequires:    %{?scl_prefix_java_common}lucene5-analysis
BuildRequires:    %{?scl_prefix}tycho
BuildRequires:    %{?scl_prefix}tycho-extras
Requires:         %{?scl_prefix}eclipse-platform >= 1:4.6.0

%description
Dynamic Languages Toolkit (DLTK) is a tool for vendors, researchers, and users
who rely on dynamic languages. DLTK is comprised of a set of extensible
frameworks designed to reduce the complexity of building full featured
development environments for dynamic languages such as PHP and Perl.

%package   ruby
Summary:   Ruby Eclipse plug-in
Requires:  ruby
#needed for ri to have standard docs so one has the basic help
Requires:  ruby-doc
%if ! 0%{?rhel}
#needed for tests runner
Requires:  rubygem-test-unit
%endif

%description ruby
Ruby development environment for Eclipse based on the Eclipse Dynamic
Languages Toolkit (DLTK).

%package   tcl
Summary:   TCL Eclipse plug-in
Requires:  tcl

%description tcl
TCL development environment for Eclipse based on the Eclipse Dynamic
Languages Toolkit (DLTK). Includes Incr TCL and XOTCL extensions.

%package   mylyn
Summary:   Mylyn integration for Eclipse DLTK projects
Requires:  %{?scl_prefix}eclipse-mylyn >= 3.21.0-4

%description mylyn
Mylyn task-focused UI integration for Eclipse Dynamic Languages Toolkit
(DLTK) projects.

%package   rse
Summary:   RSE integration for Eclipse DLTK projects

%description rse
Remote Development Support via RSE for DLTK based IDEs.

%package   sh
Summary:   Shell Script editor support
Obsoletes: %{?scl_prefix}eclipse-shelled <= 2.0.3-9.fc24
Provides:  %{?scl_prefix}eclipse-shelled = %{version}-%{release}

%description sh
Shell Script editor/launch support based on DLTK.

%package   sdk
Summary:   Eclipse DLTK SDK
Requires:  %{?scl_prefix}eclipse-pde >= 1:4.6.0
Requires:  %{name}       = %{version}-%{release}
Requires:  %{name}-ruby  = %{version}-%{release}
Requires:  %{name}-tcl   = %{version}-%{release}
Requires:  %{name}-mylyn = %{version}-%{release}
Requires:  %{name}-rse   = %{version}-%{release}
Requires:  %{name}-sh    = %{version}-%{release}

%description sdk
Documentation and source for the Eclipse Dynamic Languages Toolkit (DLTK).

%package   tests
Summary:   Eclipse DLTK Tests
Requires:  %{name}-sdk = %{version}-%{release}
Requires:  %{?scl_prefix}eclipse-swtbot

%description tests
Tests for Eclipse Dynamic Languages Toolkit (DLTK).

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n eclipse-dltk-%{gittag}

# Patch and fixes for latest lucene
pushd org.eclipse.dltk.core
%patch0 -p1
%if 0%{?rhel}
sed -i -e 's/scorer\.iterator()/scorer/' \
  core/plugins/org.eclipse.dltk.core.index.lucene/src/org/eclipse/dltk/internal/core/index/lucene/BitFlagsQuery.java
%endif
%if 0%{?fedora} < 27
sed -i -e '/	name,/d' \
  core/plugins/org.eclipse.dltk.core.index.lucene/src/org/eclipse/dltk/internal/core/index/lucene/IndexDirectory.java
sed -i -e '/SearcherFactory()/s/false,//' \
  core/plugins/org.eclipse.dltk.core.index.lucene/src/org/eclipse/dltk/internal/core/index/lucene/IndexContainer.java
%endif
popd

# We are not shipping the python and javascript editors
# For python we have eclipse-pydev, which should be used instead
# For javascript we have eclipse-webtools, which should be used instead
%pom_disable_module "../../org.eclipse.dltk.javascript" org.eclipse.dltk.releng/build/pom.xml
%pom_disable_module "../../org.eclipse.dltk.python" org.eclipse.dltk.releng/build/pom.xml
%pom_disable_module "releng/org.eclipse.dltk.core.targetplatform" org.eclipse.dltk.core/core/pom.xml

# It's not necessary to build an update site or p2 repo when using mvn_install
%pom_disable_module update.site org.eclipse.dltk.releng/build/pom.xml

sed -i '/<target>/,/<\/target>/ d' org.eclipse.dltk.core/core/tests/org.eclipse.dltk.core.tests/pom.xml

%pom_xpath_remove "pom:plugin[pom:artifactId='tycho-packaging-plugin']/pom:dependencies" org.eclipse.dltk.releng/build
%pom_xpath_remove "pom:plugin[pom:artifactId='tycho-packaging-plugin']/pom:configuration" org.eclipse.dltk.releng/build
%pom_xpath_remove "pom:plugin[pom:artifactId='target-platform-configuration']/pom:configuration/pom:target" org.eclipse.dltk.releng/build

%mvn_package "::pom::" __noinstall
%mvn_package ":*.tests" tests
%mvn_package "::jar:sources:" sdk
%mvn_package ":*.sdk" sdk
%mvn_package "org.eclipse.dltk.core:org.eclipse.dltk.core.doc.isv" sdk
%mvn_package "org.eclipse.dltk{,.core}:" core
%mvn_package "org.eclipse.dltk.ruby:" ruby
%mvn_package "org.eclipse.dltk.{tcl,itcl,xotcl}:" tcl
%mvn_package "org.eclipse.dltk.mylyn:" mylyn
%mvn_package "org.eclipse.dltk.rse:" rse
%mvn_package "org.eclipse.dltk.sh:" sh
%mvn_package "org.eclipse.dltk.features:org.eclipse.dltk.core{,.index,.index.lucene}" core
%mvn_package "org.eclipse.dltk.features:org.eclipse.dltk.ruby" ruby
%mvn_package "org.eclipse.dltk.features:org.eclipse.dltk.{tcl,itcl,xotcl}" tcl
%mvn_package "org.eclipse.dltk.features:org.eclipse.dltk.mylyn" mylyn
%mvn_package "org.eclipse.dltk.features:org.eclipse.dltk.rse" rse
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
# Qualifier generated from last modification time of source tarball
QUALIFIER=$(date -u -d"$(stat --format=%y %{SOURCE0})" +%Y%m%d%H%M)
%mvn_build -j -f -- -f org.eclipse.dltk.releng/pom.xml -DforceContextQualifier=$QUALIFIER
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles-core
%doc org.eclipse.dltk.core/core/features/org.eclipse.dltk.core-feature/rootfiles/*

%files ruby -f .mfiles-ruby
%doc org.eclipse.dltk.ruby/features/org.eclipse.dltk.ruby-feature/rootfiles/*

%files tcl -f .mfiles-tcl
%doc org.eclipse.dltk.tcl/tcl/features/org.eclipse.dltk.tcl-feature/rootfiles/*

%files mylyn -f .mfiles-mylyn
%doc org.eclipse.dltk.core/mylyn/features/org.eclipse.dltk.mylyn-feature/rootfiles/*

%files rse -f .mfiles-rse
%doc org.eclipse.dltk.core/rse/features/org.eclipse.dltk.rse-feature/rootfiles/*

%files sh -f .mfiles-sh

%files sdk -f .mfiles-sdk

%files tests -f .mfiles-tests

%changelog
* Fri Mar 31 2017 Mat Booth <mat.booth@redhat.com> - 5.7.1-1.1
- Auto SCL-ise package for rh-eclipse46 collection

* Thu Mar 30 2017 Mat Booth <mat.booth@redhat.com> - 5.7.1-1
- Update to latest upstream release
- Allow building against lucene 6

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Mat Booth <mat.booth@redhat.com> - 5.7.0-2
- Build documentation indexes using latest system version of lucene

* Tue Jan 10 2017 Mat Booth <mat.booth@redhat.com> - 5.7.0-1
- Update to latest release
- Fix indexing problems caused by split-packages in Lucene libs - rhbz#1397238
- Drop some ancient obsoletes

* Tue Oct 04 2016 Mat Booth <mat.booth@redhat.com> - 5.6.0-1
- Update to 5.6.0 release

* Thu Jul 14 2016 Mat Booth <mat.booth@redhat.com> - 5.5.0-3
- Fix restricted API warnings in lucene indexer

* Fri Jul 08 2016 Mat Booth <mat.booth@redhat.com> - 5.5.0-2
- Require fixed version of lucene-misc

* Mon Jul 04 2016 Mat Booth <mat.booth@redhat.com> - 5.5.0-1
- Update and port to latest Lucene 5

* Tue Mar 29 2016 Mat Booth <mat.booth@redhat.com> - 5.4.0-4
- Fix empty Variables view when debugging Ruby script

* Mon Mar 21 2016 Alexander Kurtakov <akurtako@redhat.com> 5.4.0-3
- Add Rs for better experience - Test:Unit run and stdlib docs.

* Fri Mar 18 2016 Mat Booth <mat.booth@redhat.com> - 5.4.0-2
- Backport patches for ebz#323736 and ebz#489902

* Mon Feb 29 2016 Alexander Kurtakov <akurtako@redhat.com> 5.4.0-1
- Update to upstream 5.4.0 release.
- Add sh subpackage obsoleting/providing eclipse-shelled (now part of DLTK).

* Wed Feb 24 2016 Sopot Cela <scela@redhat.com> - 5.3.2-3
- Fix license declaration

* Wed Feb 10 2016 Sopot Cela <scela@redhat.com> - 5.3.2-2
- Fix test package issues

* Wed Feb 10 2016 Sopot Cela <scela@redhat.com> - 5.3.2-1
- Upgrade to 5.3.2 and debugger patch

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 13 2015 Alexander Kurtakov <akurtako@redhat.com> 5.3.1-2
- Add ruby and itcl requires to the corresponding subpackages.

* Thu Oct 08 2015 Mat Booth <mat.booth@redhat.com> - 5.3.1-1
- Update to Mars.1 release
- Merge TCL packages, since they all require one another anyway

* Mon Sep 14 2015 Roland Grunberg <rgrunber@redhat.com> - 5.2.0-2
- Rebuild as an Eclipse p2 Droplet.

* Wed Jun 24 2015 Alexander Kurtakov <akurtako@redhat.com> 5.2.0-1
- Update to upstream 5.2 release.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 8 2015 Alexander Kurtakov <akurtako@redhat.com> 5.1.1-2
- Apply all Mars compatibility patches.

* Fri May 8 2015 Alexander Kurtakov <akurtako@redhat.com> 5.1.1-1
- Update to upstream 5.1.1.

* Tue Jan 20 2015 Mat Booth <mat.booth@redhat.com> - 5.1.0-6
- Make direct hamcrest use explicit in manifest

* Fri Dec 5 2014 Alexander Kurtakov <akurtako@redhat.com> 5.1.0-5
- Fix build due to unresolvable targetplatform - just skip it.

* Thu Sep 25 2014 Mat Booth <mat.booth@redhat.com> - 5.1.0-4
- Build/install with mvn_build/mvn_install
- Build and ship tests in tests sub package
- Drop unneeded BR/Rs
- Drop unneeded patch

* Wed Sep 17 2014 Alexander Kurtakov <akurtako@redhat.com> 5.1.0-3
- Drop license feature copying as it breaks the build.

* Thu Sep 04 2014 Mat Booth <mat.booth@redhat.com> - 5.1.0-2
- Unzip feature bundles on installation

* Thu Jun 26 2014 Mat Booth <mat.booth@redhat.com> - 5.1.0-1
- Update to latest upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.0-0.2.git9eca4e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Mat Booth <mat.booth@redhat.com> - 5.1.0-0.1.git9eca4e
- Update to latest upstream for Luna compatibility.
- Add BR on eclipse-license
- Drop unnecessary BR/Rs
- Build with xmvn
- Fix bogus dates

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 5.0.0-4
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 5 2013 Krzysztof Daniel <kdaniel@redhat.com> 5.0.0-3
- Fix FTBFS.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 5 2013 Alexander Kurtakov <akurtako@redhat.com> 5.0.0-1
- Update to upstream Kepler release 5.0.0.

* Thu Feb 21 2013 Alexander Kurtakov <akurtako@redhat.com> 4.0.0-5
- Let tycho skip its version checks.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 4.0.0-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Sami Wagiaalla <swagiaal@redhat.com> - 4.0.0-1
- Update to 4.0.0 release.

* Thu Jun 14 2012 Roland Grunberg <rgrunber@redhat.com> - 4.0.0-0.5.201201070225cvs
- Remove patches that bump BREE to JavaSE-1.6 (done by Tycho).
- Remove patch and %%prep lines that create p2 repository (done by Tycho).

* Thu May 03 2012 Sami Wagiaalla <swagiaal@redhat.com> - 4.0.0-0.4.201201070225cvs
- Install a symlink to h2 in dropins.
- Remove blanket symlink of javadir.

* Wed Apr 25 2012 Sami Wagiaalla <swagiaal@redhat.com> - 4.0.0-0.3.201201070225cvs
- Install missing bundles.

* Tue Apr 24 2012 Sami Wagiaalla <swagiaal@redhat.com> - 4.0.0-0.2.201201070225cvs
- Checkout entire org.eclipse.dltk module.
- Patch dltk to build with tycho 0.14.0
- Use tycho to build dltk
- Add tycho and maven requirements.

* Thu Apr 12 2012 Sami Wagiaalla <swagiaal@redhat.com> - 4.0.0-0.1.201201070225cvs
- Update to upstream 4.0.0 snapshot.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 16 2011 Alexander Kurtakov <akurtako@redhat.com> 3.0.1-1
- Update to upstream 3.0.1.

* Tue Jul 12 2011 Alexander Kurtakov <akurtako@redhat.com> 3.0-2
- Add more mylyn subpackages to BR/R.

* Tue Jul 12 2011 Alexander Kurtakov <akurtako@redhat.com> 3.0-1
- Update to upstream 3.0.

* Tue Jul 5 2011 Andrew Overholt <overholt@redhat.com> 2.0.1-4
- Update dropins locations to reflect Mylyn split.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 6 2010 Alexander Kurtakov <akurtako@redhat.com> 2.0.1-2
- BR/R h2 and fix build.

* Tue Oct 19 2010 Chris Aniszczyk <zx@redhat.com> 2.0.1-1
- Update to 2.0.1.

* Sun Jul 18 2010 Alexander Kurtakov <akurtako@redhat.com> 2.0.0-1
- Update to 2.0.0.

* Wed Mar 03 2010 Mat Booth <fedora@matbooth.co.uk> 1.0.2-1
- Update to 1.0.2

* Wed Jan 20 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0.0-4
- Main package should require emf.

* Thu Aug 20 2009 Mat Booth <fedora@matbooth.co.uk> 1.0.0-3
- Add a SDK package.
- Require Mylyn >= 3.2.

* Mon Aug 10 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0.0-2
- Add RSE plugin.

* Mon Aug 10 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0.0-1
- Update to 1.0.0 final.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.6.RC1b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0.0-0.5.RC1b
- Update to 1.0.0 RC1b.
- Use %%global instead of %%define.

* Sat Apr 18 2009 Mat Booth <fedora@matbooth.co.uk> 1.0.0-0.4.M6
- Update to Milestone 6 release of 1.0.0.
- Require Eclipse 3.5.0.

* Thu Apr 02 2009 Mat Booth <fedora@matbooth.co.uk> 1.0.0-0.3.M5
- Fix files listed twice warnings.

* Thu Apr 02 2009 Mat Booth <fedora@matbooth.co.uk> 1.0.0-0.2.M5
- Drop GCJ AOT support.

* Mon Mar 30 2009 Mat Booth <fedora@matbooth.co.uk> 1.0.0-0.1.M5
- Initial release.