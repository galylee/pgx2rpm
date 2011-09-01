# This spec file and ancilliary files are licensed in accordance with 
# The PostgreSQL license.

# In this file you can find the default build package list macros.
# These can be overridden by defining on the rpm command line:
# rpm --define 'packagename 1' .... to force the package to build.
# rpm --define 'packagename 0' .... to force the package NOT to build.
# The base package, the lib package, the devel package, and the server package
# always get built.

%define _prefix /opt/pgxc
%define _bindir %{_prefix}/bin
%define _libdir %{_prefix}/lib
%define _docdir %{_prefix}/share/doc
%define _mandir %{_prefix}/share/man
%define _datadir %{_prefix}/share

%define __check_files %{nil}

%global beta 0
%{?beta:%global __os_install_post /usr/lib/rpm/brp-compress}

%{!?tcldevel:%global tcldevel 1}
%{!?plpython:%global plpython 1}
%{!?pltcl:%global pltcl 1}
%{!?plperl:%global plperl 1}
%{!?ssl:%global ssl 1}
%{!?kerberos:%global kerberos 1}
%{!?ldap:%global ldap 1}
%{!?uuid:%global uuid 1}
%{!?xml:%global xml 1}
%{!?pam:%global pam 1}
%{!?sdt:%global sdt 1}
%{!?pgfts:%global pgfts 1}

Summary: Postgres-XC client programs and libraries
Name: postgres-xc
Version: 0.9.5
Release: 1%{?dist}
# The PostgreSQL license is very similar to other MIT licenses, but the OSI
# recognizes it as an independent license, so we do as well.
License: PostgreSQL
Group: Applications/Databases
Url: http://postgres-xc.sourceforge.net/

Source0: http://sourceforge.net/projects/postgres-xc/files/Version_%{version}/pgxc-%{version}.tar.gz
#Source1: postgres-xc-A4.pdf
Source14: postgres-xc.pam

# Comments for these patches are in the patch files.


BuildRequires: perl(ExtUtils::MakeMaker) glibc-devel bison flex gawk
BuildRequires: perl(ExtUtils::Embed), perl
Requires(post): glibc
Requires(postun): glibc

%if %plpython
BuildRequires: python-devel
%endif

%if %pltcl
BuildRequires: tcl
%define _tclconfig_dir /usr/lib64
%if %tcldevel
BuildRequires: tcl-devel
%endif
%endif

BuildRequires: readline-devel
BuildRequires: zlib-devel >= 1.0.4

%if %ssl
BuildRequires: openssl-devel
%endif

%if %kerberos
BuildRequires: krb5-devel
%endif

%if %ldap
BuildRequires: openldap-devel
%endif

%if %uuid
BuildRequires: uuid-devel
%endif

%if %xml
BuildRequires: libxml2-devel libxslt-devel
%endif

%if %pam
BuildRequires: pam-devel
%endif

%if %sdt
BuildRequires: systemtap-sdt-devel
%endif

# main package requires -libs subpackage
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
PostgreSQL is an advanced Object-Relational database management system
(DBMS) that supports almost all SQL constructs (including
transactions, sub-selects and user-defined types and functions). The
postgresql-xc package includes the client programs and libraries that
you'll need to access a PostgreSQL DBMS server.  These PostgreSQL
client programs are programs that directly manipulate the internal
structure of PostgreSQL databases on a PostgreSQL server. These client
programs can be located on the same machine with the PostgreSQL
server, or may be on a remote machine which accesses a PostgreSQL
server over a network connection. This package contains the docs
in HTML for the whole package, as well as command-line utilities for
managing PostgreSQL databases on a PostgreSQL server. 

If you want to manipulate a PostgreSQL database on a local or remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the postgresql-server package.

%package libs
Summary: The shared libraries required for any Postgres-XC clients
Group: Applications/Databases
Provides: libpq.so = %{version}-%{release}

%description libs
The postgres-xc-libs package provides the essential shared libraries for any 
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package server
Summary: The programs needed to create and run a Postgres-XC server
Group: Applications/Databases
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description server
The postgres-xc-server package includes the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.  PostgreSQL is an advanced
Object-Relational database management system (DBMS) that supports
almost all SQL constructs (including transactions, sub-selects and
user-defined types and functions). You should install
postgresql-server if you want to create and maintain your own
PostgreSQL databases and/or your own PostgreSQL server. You also need
to install the postgresql package.


#%package docs
#Summary: Extra documentation for Postgres-XC
#Group: Applications/Databases
#Requires: %{name}%{?_isa} = %{version}-%{release}
#
#%description docs
#The postgres-xc-docs package includes some additional documentation for
#PostgreSQL.  Currently, this includes the main documentation in PDF format.


%package contrib
Summary: Contributed modules distributed with Postgres-XC
Group: Applications/Databases
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description contrib
The postgres-xc-contrib package contains contributed packages that are
included in the PostgreSQL distribution.


%package devel
Summary: Postgres-XC development header files and libraries
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The postgres-xc-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server and the ecpg Embedded C
Postgres preprocessor. You need to install this package if you want to
develop applications which will interact with a PostgreSQL server.


%if %plperl
%package plperl
Summary: The Perl procedural language for Postgres-XC
Group: Applications/Databases
Requires: %{name}-server%{?_isa} = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description plperl
PostgreSQL is an advanced Object-Relational database management
system.  The postgres-xc-plperl package contains the PL/Perl
procedural language for the backend.
%endif

%if %plpython
%package plpython
Summary: The Python procedural language for Postgres-XC
Group: Applications/Databases
Requires: %{name}-server%{?_isa} = %{version}-%{release}

%description plpython
PostgreSQL is an advanced Object-Relational database management
system.  The postgres-xc-plpython package contains the PL/Python
procedural language for the backend.
%endif

%if %pltcl
%package pltcl
Summary: The Tcl procedural language for Postgres-XC
Group: Applications/Databases
Requires: %{name}-server%{?_isa} = %{version}-%{release}

%description pltcl
PostgreSQL is an advanced Object-Relational database management
system.  The postgres-xc-pltcl package contains the PL/Tcl
procedural language for the backend.
%endif

%prep
%setup -q -n pgxc-%{version}

#cp -p %{SOURCE1} .

# remove .gitignore files to ensure none get into the RPMs (bug #642210)
find . -type f -name .gitignore | xargs rm

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS

# Strip out -ffast-math from CFLAGS....
CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
# Add LINUX_OOM_ADJ=0 to ensure child processes reset postmaster's oom_adj
CFLAGS="$CFLAGS -DLINUX_OOM_ADJ=0"

%configure --disable-rpath \
%if %beta
	--enable-debug \
	--enable-cassert \
%endif
%if %plperl
	--with-perl \
%endif
%if %pltcl
	--with-tcl \
	--with-tclconfig=%{_tclconfig_dir} \
%endif
%if %plpython
	--with-python \
%endif
%if %ldap
	--with-ldap \
%endif
%if %ssl
	--with-openssl \
%endif
%if %pam
	--with-pam \
%endif
%if %kerberos
	--with-krb5 \
	--with-gssapi \
%endif
%if %uuid
	--with-ossp-uuid \
%endif
%if %xml
	--with-libxml \
	--with-libxslt \
%endif
%if %sdt
	--enable-dtrace \
%endif
%if %pgfts
	--enable-thread-safety \
%endif
	--with-system-tzdata=/usr/share/zoneinfo

#make %{?_smp_mflags} world
make %{?_smp_mflags} all
make %{?_smp_mflags} -C contrib

%install
rm -rf $RPM_BUILD_ROOT

#make DESTDIR=$RPM_BUILD_ROOT install-world
make DESTDIR=$RPM_BUILD_ROOT install
make DESTDIR=$RPM_BUILD_ROOT -C contrib install

%if %pam
install -d $RPM_BUILD_ROOT/etc/pam.d
install -m 644 %{SOURCE14} $RPM_BUILD_ROOT/etc/pam.d/postgres-xc
%endif

#mv $RPM_BUILD_ROOT%{_docdir}/postgresql/html doc
#rm -rf $RPM_BUILD_ROOT%{_docdir}/postgresql

# remove files not to be packaged
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

# FILES section.

%files
%defattr(-,root,root)
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES doc/README* 
%doc COPYRIGHT README HISTORY doc/bug.template
#%doc doc/html
%{_bindir}/clusterdb
%{_bindir}/createdb
%{_bindir}/createlang
%{_bindir}/createuser
%{_bindir}/dropdb
%{_bindir}/droplang
%{_bindir}/dropuser
%{_bindir}/pg_config
%{_bindir}/pg_dump
%{_bindir}/pg_dumpall
%{_bindir}/pg_restore
%{_bindir}/psql
%{_bindir}/reindexdb
%{_bindir}/vacuumdb
# GTM binaries
%{_bindir}/gtm
%{_bindir}/gtm_proxy
%{_bindir}/gtm_ctl
#%{_mandir}/man1/clusterdb.*
#%{_mandir}/man1/createdb.*
#%{_mandir}/man1/createlang.*
#%{_mandir}/man1/createuser.*
#%{_mandir}/man1/dropdb.*
#%{_mandir}/man1/droplang.*
#%{_mandir}/man1/dropuser.*
#%{_mandir}/man1/pg_config.*
#%{_mandir}/man1/pg_dump.*
#%{_mandir}/man1/pg_dumpall.*
#%{_mandir}/man1/pg_restore.*
#%{_mandir}/man1/psql.*
#%{_mandir}/man1/reindexdb.*
#%{_mandir}/man1/vacuumdb.*
#%{_mandir}/man7/*
%dir %{_libdir}/postgresql


#%files docs
#%defattr(-,root,root)
#%doc *-A4.pdf


%files contrib
%defattr(-,root,root)
%{_libdir}/postgresql/_int.so
%{_libdir}/postgresql/adminpack.so
%{_libdir}/postgresql/autoinc.so
%{_libdir}/postgresql/auto_explain.so
%{_libdir}/postgresql/btree_gin.so
%{_libdir}/postgresql/btree_gist.so
%{_libdir}/postgresql/chkpass.so
%{_libdir}/postgresql/citext.so
%{_libdir}/postgresql/cube.so
%{_libdir}/postgresql/dblink.so
%{_libdir}/postgresql/dict_int.so
%{_libdir}/postgresql/dict_xsyn.so
%{_libdir}/postgresql/earthdistance.so
%{_libdir}/postgresql/fuzzystrmatch.so
%{_libdir}/postgresql/hstore.so
%{_libdir}/postgresql/insert_username.so
%{_libdir}/postgresql/isn.so
#%{_libdir}/postgresql/lo.so
%{_libdir}/postgresql/ltree.so
%{_libdir}/postgresql/moddatetime.so
%{_libdir}/postgresql/pageinspect.so
%{_libdir}/postgresql/passwordcheck.so
%{_libdir}/postgresql/pg_buffercache.so
%{_libdir}/postgresql/pg_freespacemap.so
%{_libdir}/postgresql/pg_trgm.so
%{_libdir}/postgresql/pgcrypto.so
%{_libdir}/postgresql/pgrowlocks.so
%{_libdir}/postgresql/pgstattuple.so
#%{_libdir}/postgresql/pg_stat_statements.so
%{_libdir}/postgresql/refint.so
%{_libdir}/postgresql/seg.so
%{_libdir}/postgresql/sslinfo.so
%{_libdir}/postgresql/tablefunc.so
%{_libdir}/postgresql/test_parser.so
%{_libdir}/postgresql/timetravel.so
%{_libdir}/postgresql/tsearch2.so
%{_libdir}/postgresql/unaccent.so
%if %uuid
%{_libdir}/postgresql/uuid-ossp.so
%endif
%if %xml
%{_libdir}/postgresql/pgxml.so
%endif
%{_datadir}/postgresql/contrib/
%{_bindir}/oid2name
%{_bindir}/pg_archivecleanup
%{_bindir}/pg_standby
%{_bindir}/pgbench
#%{_bindir}/vacuumlo
#%{_mandir}/man3/dblink*
%doc contrib/spi/*.example


%files libs
%defattr(-,root,root)
%doc COPYRIGHT
%{_libdir}/libpq.so.*
%{_libdir}/libecpg.so.*
%{_libdir}/libpgtypes.so.*
%{_libdir}/libecpg_compat.so.*


%files server
%defattr(-,root,root)
%if %pam
%config(noreplace) /etc/pam.d/postgres-xc
%endif
%{_bindir}/initdb
%{_bindir}/pg_controldata
%{_bindir}/pg_ctl
%{_bindir}/pg_resetxlog
%{_bindir}/postgres
%{_bindir}/postmaster
%{_bindir}/gtm
%{_bindir}/gtm_ctl
%{_bindir}/gtm_proxy
#%{_mandir}/man1/initdb.*
#%{_mandir}/man1/pg_controldata.*
#%{_mandir}/man1/pg_ctl.*
#%{_mandir}/man1/pg_resetxlog.*
#%{_mandir}/man1/postgres.*
#%{_mandir}/man1/postmaster.*
%{_datadir}/postgresql/postgres.bki
%{_datadir}/postgresql/postgres.description
%{_datadir}/postgresql/postgres.shdescription
%{_datadir}/postgresql/system_views.sql
%{_datadir}/postgresql/*.sample
%{_datadir}/postgresql/timezonesets/
%{_datadir}/postgresql/tsearch_data/
%{_libdir}/postgresql/dict_snowball.so
%{_libdir}/postgresql/plpgsql.so
%dir %{_datadir}/postgresql
%{_libdir}/postgresql/libpqwalreceiver.so
%{_libdir}/postgresql/*_and_*.so
%{_libdir}/postgresql/euc2004_sjis2004.so
%{_datadir}/postgresql/conversion_create.sql
%{_datadir}/postgresql/information_schema.sql
%{_datadir}/postgresql/snowball_create.sql
%{_datadir}/postgresql/sql_features.txt


%files devel
%defattr(-,root,root)
%{_prefix}/include/*
%{_bindir}/ecpg
%{_libdir}/libpq.so
%{_libdir}/libecpg.so
%{_libdir}/libecpg_compat.so
%{_libdir}/libpgtypes.so
%{_libdir}/postgresql/pgxs/
#%{_mandir}/man1/ecpg.*
#%{_mandir}/man3/SPI_*

%if %plperl
%files plperl
%defattr(-,root,root)
%{_libdir}/postgresql/plperl.so
%endif

%if %pltcl
%files pltcl
%defattr(-,root,root)
%{_libdir}/postgresql/pltcl.so
%{_bindir}/pltcl_delmod
%{_bindir}/pltcl_listmod
%{_bindir}/pltcl_loadmod
%{_datadir}/postgresql/unknown.pltcl
%endif

%if %plpython
%files plpython
%defattr(-,root,root)
%{_libdir}/postgresql/plpython.so
%{_libdir}/postgresql/plpython2.so
%endif

%changelog
* Mon Aug 30 2011 Nippon Telegraph and Telephone Corporation - v0.9.5-1
- initial rpm package

