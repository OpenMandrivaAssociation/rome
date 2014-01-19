%{?_javapackages_macros:%_javapackages_macros}
Name:		rome
Version:	0.9
Release:	14.0%{?dist}
Summary:	RSS and Atom Utilities


License:	ASL 2.0
URL:		https://rome.dev.java.net/
# wget https://rome.dev.java.net/source/browse/*checkout*/rome/www/dist/rome-0.9-src.tar.gz?rev=1.1
Source0:	%{name}-%{version}-src.tar.gz
# wget http://download.eclipse.org/tools/orbit/downloads/drops/R20090825191606/bundles/com.sun.syndication_0.9.0.v200803061811.jar
# unzip com.sun.syndication_0.9.0.v200803061811.jar META-INF/MANIFEST.MF
# sed -i 's/\r//' META-INF/MANIFEST.MF
# # We won't have the same SHA-1 sums (class sometimes spills into # cl\nass)
# sed -i -e "/^Name/d" -e "/^SHA/d" -e "/^\ ass$/d" -e "/^$/d" META-INF/MANIFEST.MF
Source1:	MANIFEST.MF
Source2:    http://repo1.maven.org/maven2/%{name}/%{name}/%{version}/%{name}-%{version}.pom
BuildArch:	noarch

Patch0:		%{name}-%{version}-addosgimanifest.patch
# fix maven-surefire-plugin aId
Patch1:     %{name}-%{version}-pom.patch

BuildRequires:	java-devel >= 1:1.7.0
BuildRequires:	jpackage-utils
BuildRequires:	ant
BuildRequires:	jdom >= 1.1.2-3
Requires:	java >= 1:1.7.0
Requires:	jpackage-utils
Requires:	jdom >= 1.1.2-3

%description
ROME is an set of open source Java tools for parsing, generating and
publishing RSS and Atom feeds.

%package	javadoc
Summary:	Javadocs for %{name}

Requires:	%{name} = %{version}-%{release}
Requires:	jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q
find -name '*.jar' -o -name '*.class' -exec rm -f '{}' \;
mkdir -p target/lib
ln -s %{_javadir}/jdom.jar target/lib
cp -p %{SOURCE1} .
%patch0
cp -p %{SOURCE2} pom.xml
%patch1

%build
ant -Dnoget=true dist

%install
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p target/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

mkdir -p $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp dist/docs/api/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 gil cattaneo <puntogil@libero.it> 0.9-11
- Added maven POM

* Tue Apr 17 2012 Alexander Kurtakov <akurtako@redhat.com> 0.9-10
- Adapt to current guidelines.

* Fri Apr 13 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.9-9
- Use Java 7
- Use latest jdom

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 15 2010 Alexander Kurtakov <akurtako@redhat.com> 0.9-6
- Fix build with latest jdom. (rhbz#565057)

* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0.9-5
- Update URL in instructions for getting MANIFEST.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 30 2009 Andrew Overholt <overholt@redhat.com> 0.9-3
- Fix javadoc Group (rhbz#492761).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 25 2008 Andrew Overholt <overholt@redhat.com> 0.9-1
- Initial Fedora version
