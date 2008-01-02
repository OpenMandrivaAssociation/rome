%define section         free
%define gcj_support     1

Name:           rome
Version:        0.9
Release:        %mkrel 1.0.4
Epoch:          0
Summary:        RSS and Atom Utilities for Java
License:        Apache License
Group:          Development/Java
URL:            https://rome.dev.java.net/
Source0:        https://rome.dev.java.net/source/browse/*checkout*/rome/www/dist/rome-0.9-src.zip
Requires:       jdom
Requires:       jpackage-utils >= 0:1.6
BuildRequires:  ant
BuildRequires:  jdom
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  junit
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
ROME is an open source (Apache license) set of Atom/RSS Java
utilities that make it easy to work in Java with most syndication
formats:

RSS 0.90, RSS 0.91 Netscape, RSS 0.91 Userland, RSS 0.92, RSS 0.93,
RSS 0.94, RSS 1.0, RSS 2.0, Atom 0.3, and Atom 1.0.

ROME includes a set of parsers and generators for the various flavors
of syndication feeds, as well as converters to convert from one
format to another. The parsers can give you back Java objects that
are either specific for the format you want to work with, or a
generic normalized SyndFeed class that lets you work on with the
data without bothering about the incoming or outgoing feed type.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%{__mkdir_p} target/lib
%{__perl} -pi -e 's|<javac|<javac nowarn="true"|g' build.xml

%build
export CLASSPATH=$(build-classpath jdom junit)
export OPT_JAR_LIST=:
%{ant} -Djdom=$(build-classpath jdom) jar javadoc compile-tests

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%check
export CLASSPATH=$(build-classpath jdom junit)
export OPT_JAR_LIST="ant/ant-junit"
%{ant} -Djdom=$(build-classpath jdom) internal-test || :

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.db
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.so
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %dir %{_javadocdir}/%{name}
