%define gtest_version 1.7.0
%global _disable_rebuild_configure 1

# Major
%define major %(echo %{version}|cut -d. -f1)

# Library names
%define libname %mklibname %{name}
%define liblite %mklibname %{name}-lite
%define libcompiler %mklibname protoc
%define devname %mklibname %{name} -d
%define sdevname %mklibname %{name} -d -s

%bcond_without python

# Java stack is not supported on x86_32
%ifarch %{ix86}
%bcond_with java
%else
%bcond_with java
%endif

%bcond_with gtest

Summary:	Protocol Buffers - Google's data interchange format
Name:		protobuf
Version:	25.2
Release:	1
License:	BSD
Group:		Development/Other
Url:		https://github.com/protocolbuffers/protobuf
Source0:	https://github.com/protocolbuffers/protobuf/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	ftdetect-proto.vim
Patch1:		protobuf-22.4-soname.patch
Patch2:		protobuf-23.0-workaround-pkgconfig-infinite-loop.patch
# Some Python binding tests are broken in 24.0
# (build failure -- google/protobuf/unittest_arena.proto: is an editions file,
# but code generator --python_out hasn't been updated to support editions yet.)
# Disable them for now.
#Patch3:		protobuf-24.0-python-disable-broken-tests.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	pkgconfig(zlib)
BuildRequires:	cmake(absl)
%if %{with gtest}
BuildRequires:	gtest-devel
%endif
%if %{with python}
BuildRequires:	pkgconfig(python)
BuildRequires:	python-setuptools
%endif
%if %{with java}
BuildRequires:	java-devel >= 1.6
BuildRequires:	jpackage-utils
BuildRequires:	maven-local
BuildRequires:	mvn(com.google.code.gson:gson)
BuildRequires:	mvn(com.google.guava:guava)
BuildRequires:	mvn(junit:junit)
BuildRequires:	mvn(org.easymock:easymock)
BuildRequires:	mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:	mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:	mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:	mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:	maven-compiler-plugin
BuildRequires:	maven-install-plugin
BuildRequires:	maven-jar-plugin
BuildRequires:	maven-javadoc-plugin
BuildRequires:	maven-release-plugin
BuildRequires:	maven-resources-plugin
BuildRequires:	maven-surefire-plugin
BuildRequires:	maven-antrun-plugin
%endif

%description
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

Protocol buffers are a flexible, efficient, automated mechanism for
serializing structured data - think XML, but smaller, faster, and
simpler. You define how you want your data to be structured once, then
you can use special generated source code to easily write and read
your structured data to and from a variety of data streams and using a
variety of languages. You can even update your data structure without
breaking deployed programs that are compiled against the "old" format.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Runtime library for %{name}
Group:		System/Libraries

%description -n %{libname}
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

Protocol buffers are a flexible, efficient, automated mechanism for
serializing structured data - think XML, but smaller, faster, and
simpler. You define how you want your data to be structured once, then
you can use special generated source code to easily write and read
your structured data to and from a variety of data streams and using a
variety of languages. You can even update your data structure without
breaking deployed programs that are compiled against the "old" format.

This package contains the shared %{name} library.

%files -n %{libname}
%doc CONTRIBUTORS.txt LICENSE README.md
%{_libdir}/lib%{name}.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{liblite}
Summary:	Protocol Buffers lite version
Group:		Development/Other

%description -n %{liblite}
This package contains a compiled with "optimize_for = LITE_RUNTIME"
version of Google's Protocol Buffers library.

The "optimize_for = LITE_RUNTIME" option causes the compiler to
generate code which only depends libprotobuf-lite, which is much
smaller than libprotobuf but lacks descriptors, reflection, and some
other features.

%files -n %{liblite}
%doc LICENSE README.md
%{_libdir}/lib%{name}-lite.so.%{major}*

#----------------------------------------------------------------------------

%package compiler
Summary:	Protocol Buffers compiler
Group:		Development/Other
Recommends:	%{libname}
Recommends:	%{liblite}

%description compiler
This package contains Protocol Buffers compiler for all programming
languages.

%files compiler
%doc LICENSE README.md
%{_bindir}/protoc
%{_bindir}/protoc-%{version}*

#----------------------------------------------------------------------------

%package -n %{libcompiler}
Summary:	Protocol Buffers compiler shared library
Group:		System/Libraries

%description -n %{libcompiler}
This package contains the Protocol Buffers compiler shared library.

%files -n %{libcompiler}
%{_libdir}/libprotoc.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Protocol Buffers C++ headers and libraries
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Requires:	%{liblite} = %{EVRD}
Requires:	%{libcompiler} = %{EVRD}
Requires:	%{name}-compiler = %{EVRD}
# protobuf is heavily dependent on absl these days
Requires:	cmake(absl)
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
This package contains Protocol Buffers compiler for all languages and
C++ headers and libraries.

%files -n %{devname}
%doc examples/add_person.cc examples/addressbook.proto
%doc examples/list_people.cc examples/Makefile examples/README.md
%dir %{_includedir}/google
%{_includedir}/google/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}-lite.so
%{_libdir}/libprotoc.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-lite.pc
%{_includedir}/utf8_*.h
%{_libdir}/cmake/protobuf
%{_libdir}/cmake/utf8_range
%{_libdir}/libutf8_range.a
%{_libdir}/libutf8_validity.a
%{_libdir}/pkgconfig/utf8_range.pc

#----------------------------------------------------------------------------

%package -n %{sdevname}
Summary:	Static development files for %{name}
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Requires:	%{liblite} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}

%description -n %{sdevname}
This package contains static libraries for Protocol Buffers.

%files -n %{sdevname}
%{_libdir}/lib%{name}.a
%{_libdir}/lib%{name}-lite.a
%{_libdir}/libprotoc.a

#----------------------------------------------------------------------------

%if %{with python}
%package -n python-%{name}
Summary:	Python 3 bindings for Google Protocol Buffers
Group:		Development/Python
Requires:	%{name}-compiler = %{EVRD}

%description -n python-%{name}
This package contains Python 3 bindings for Google Protocol Buffers.

%files -n python-%{name}
%doc python/README.md
%doc examples/add_person.py examples/list_people.py examples/addressbook.proto
%dir %{python_sitelib}/google
%{python_sitelib}/google/%{name}/
%{python_sitelib}/%{name}-*-py%{python_version}.egg-info/
%{python_sitelib}/%{name}-*-py%{python_version}-nspkg.pth
%endif

#----------------------------------------------------------------------------

%package vim
Summary:	Vim syntax highlighting for Google Protocol Buffers
Group:		Development/Other
Requires:	vim-enhanced

%description vim
This package contains syntax highlighting for Google Protocol Buffers
descriptions in Vim editor.

%files vim
%{_datadir}/vim/vimfiles/ftdetect/proto.vim
%{_datadir}/vim/vimfiles/syntax/proto.vim

#----------------------------------------------------------------------------

%if %{with java}
%package java
Summary:	Java Protocol Buffers runtime library
Group:		Development/Java
Requires:	java
Requires:	jpackage-utils
Requires(post,postun):	jpackage-utils
Requires:	%{name}-compiler = %{EVRD}

%description java
This package contains Java Protocol Buffers runtime library.

%files java -f .mfiles-protobuf-java
%doc examples/AddPerson.java examples/ListPeople.java
%doc java/README.md
%doc LICENSE
%{_includedir}/java/core/src/main/java/com/google/protobuf/java_features.proto

#----------------------------------------------------------------------------

%package javalite
Summary:	Java Protocol Buffers lite runtime library
BuildArch:	noarch

%description javalite
This package contains Java Protocol Buffers lite runtime library.

%files javalite -f .mfiles-protobuf-javalite
%doc LICENSE

#----------------------------------------------------------------------------

%package java-util
Summary:	Utilities for Protocol Buffers
BuildArch:	noarch

%description java-util
Utilities to work with protos. It contains JSON support
as well as utilities to work with proto3 well-known types.

%files java-util -f .mfiles-protobuf-java-util

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}-java
BuildArch:	noarch

%description javadoc
This package contains the API documentation for %{name}-java.

%files javadoc -f .mfiles-javadoc
%doc LICENSE

#----------------------------------------------------------------------------

%package parent
Summary:	Protocol Buffer Parent POM
BuildArch:	noarch

%description parent
Protocol Buffer Parent POM.

%files parent -f .mfiles-protobuf-parent
%doc LICENSE

#----------------------------------------------------------------------------


%package bom
Summary:	Protocol Buffer BOM POM
BuildArch:	noarch

%description bom
Protocol Buffer BOM POM.

%files bom -f .mfiles-protobuf-bom
%doc LICENSE

%endif
#----------------------------------------------------------------------------

%prep
%autosetup -p1

%if %{with java}
%pom_remove_dep org.easymock:easymockclassextension java/pom.xml java/core/pom.xml java/lite/pom.xml java/util/pom.xml
%pom_remove_dep com.google.truth:truth java/pom.xml java/core/pom.xml java/lite/pom.xml java/util/pom.xml
%pom_remove_dep com.google.errorprone:error_prone_annotations java/util/pom.xml
%pom_remove_dep com.google.guava:guava-testlib java/pom.xml java/util/pom.xml
# These use easymockclassextension
rm java/core/src/test/java/com/google/protobuf/ServiceTest.java
# These use truth or error_prone_annotations or guava-testlib
rm java/core/src/test/java/com/google/protobuf/LiteralByteStringTest.java
rm java/core/src/test/java/com/google/protobuf/BoundedByteStringTest.java
rm java/core/src/test/java/com/google/protobuf/RopeByteStringTest.java
rm java/core/src/test/java/com/google/protobuf/RopeByteStringSubstringTest.java
rm -r java/util/src/test/java/com/google/protobuf/util
rm -r java/util/src/main/java/com/google/protobuf/util

# Make OSGi dependency on sun.misc package optional
%pom_xpath_inject "pom:configuration/pom:instructions" "<Import-Package>sun.misc;resolution:=optional,*</Import-Package>" java/core

# Backward compatibility symlink
%mvn_file :protobuf-java:jar: %{name}/%{name}-java %{name}
%endif

# Avoid dependencies
chmod 644 examples/*.py

# FIXME we currently disable BUILD_TESTS because of its
# dependency on absl::scoped_mock_log, which doesn't exist
# in any released version of abseil-cpp. Enable tests on
# next absl upstream release.
%cmake \
	-Dprotobuf_BUILD_EXAMPLES:BOOL=ON \
	-Dprotobuf_BUILD_LIBPROTOC:BOOL=ON \
	-Dprotobuf_BUILD_SHARED_LIBS:BOOL=ON \
	-Dprotobuf_USE_EXTERNAL_GTEST:BOOL=ON \
	-Dprotobuf_ABSL_PROVIDER=package \
	-Dprotobuf_BUILD_TESTS:BOOL=OFF \
	-G Ninja

cd ..
export CMAKE_BUILD_DIR=build-static
%cmake \
	-Dprotobuf_BUILD_EXAMPLES:BOOL=ON \
	-Dprotobuf_BUILD_LIBPROTOC:BOOL=ON \
	-Dprotobuf_BUILD_SHARED_LIBS:BOOL=OFF \
	-Dprotobuf_USE_EXTERNAL_GTEST:BOOL=ON \
	-Dprotobuf_ABSL_PROVIDER=package \
	-Dprotobuf_BUILD_TESTS:BOOL=OFF \
	-G Ninja

%build
%ninja_build -C build
%ninja_build -C build-static

# Use the just built protoc instead of any
# system version for python and/or java bindings
export PROTOC=$(pwd)/build-static/protoc

%if %{with python}
pushd python
%__python ./setup.py build
sed -i -e 1d build/lib/google/protobuf/descriptor_pb2.py
popd
%endif

%if %{with java}
%mvn_build -s -- -f java/pom.xml
%endif

%install
%ninja_install -C build-static
%ninja_install -C build

%if %{with python}
pushd python
%__python ./setup.py install --root=%{buildroot} --single-version-externally-managed --record=INSTALLED_FILES --optimize=1
popd
%endif

install -p -m 644 -D %{SOURCE1} %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/proto.vim
install -p -m 644 -D editors/proto.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/proto.vim

%if %{with java}
%mvn_install
%else
rm -rf %{buildroot}%{_includedir}/java
%endif

#check
# Tests are looking for yet another googletest setup in third_party/googletest
#make_build check
