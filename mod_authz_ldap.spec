
Summary: LDAP authorization module for the Apache HTTP Server
Name: mod_authz_ldap
Version: 0.26
Release: 15%{?dist}
License: BSD
Group: System Environment/Daemons
URL: http://authzldap.othello.ch/
Source0: http://authzldap.othello.ch/download/%{name}-%{version}.tar.gz
Source1: mod_authz_ldap.conf
Patch1: mod_authz_ldap-0.22-hook.patch
Patch2: mod_authz_ldap-0.22-passlog.patch
Patch3: mod_authz_ldap-0.25-build.patch
Patch4: mod_authz_ldap-0.26-subreq.patch
Patch5: mod_authz_ldap-0.26-apr1x.patch
Patch6: mod_authz_ldap-0.26-parser.patch
Patch7: mod_authz_ldap-0.26-sslvar.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: httpd-devel, openssl-devel, openldap-devel
Requires: httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo httpd-devel missing)
Requires: openldap
Obsoletes: auth_ldap

%description
The mod_authz_ldap package provides support for authenticating
users of the Apache HTTP server against an LDAP database.
mod_authz_ldap features the ability to authenticate users based on
the SSL client certificate presented, and also supports password
aging, and authentication based on role or by configured filters.

%prep
%setup -q
%patch1 -p1 -b .hook
%patch2 -p1 -b .passlog
%patch3 -p1 -b .build
%patch4 -p1 -b .subreq
%patch5 -p1 -b .apr1x
%patch6 -p1 -b .parser
%patch7 -p1 -b .sslvar

%build
libtoolize --copy --force && aclocal && autoconf
export CPPFLAGS="`apu-1-config --includes` -I%{_includedir}/openssl -DLDAP_DEPRECATED=1"
%configure --with-apxs=%{_sbindir}/apxs --disable-static
cd module
%{_sbindir}/apxs -Wl,-export-symbols-regex -Wl,authz_ldap_module \
         -Wc,-DAUTHZ_LDAP_HAVE_SSL -c -o mod_authz_ldap.la *.c \
         -Wl,-lldap -Wl,-lcrypto

%install
rm -rf $RPM_BUILD_ROOT

make -C tools install DESTDIR=$RPM_BUILD_ROOT
make -C docs install DESTDIR=$RPM_BUILD_ROOT

# install the DSO
mkdir -p $RPM_BUILD_ROOT%{_libdir}/httpd/modules
install -m 755 module/.libs/mod_authz_ldap.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules

# install the conf.d fragment
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -p -m 644 %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/authz_ldap.conf

rm -f $RPM_BUILD_ROOT%{_libdir}/httpd/modules/{*.la,*.so.*}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/authz_ldap.conf
%{_libdir}/httpd/modules/*.so
%{_bindir}/cert*
%{_mandir}/man1/cert*
%doc ldap/*.schema docs/*.{html,jpg} docs/*.{HOWTO,txt} docs/README
%doc NEWS AUTHORS ChangeLog COPYING

%changelog
* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.26-15
- rebuilt with new openssl

* Fri Aug 07 2009 Parag <paragn@fedoraproject.org> 0.26-14
- Spec cleanup as suggested in review bug #226154

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.26-11
- rebuild with new openssl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.26-10
- Autorebuild for GCC 4.3

* Thu Dec  6 2007 Joe Orton <jorton@redhat.com> 0.26-9
- rebuild for new OpenLDAP

* Thu Mar 22 2007 Joe Orton <jorton@redhat.com> 0.26-8
- add fix for filter paranthesis parsing
- update example configurations

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 0.26-7.1
- rebuild

* Mon Mar 27 2006 Joe Orton <jorton@redhat.com> 0.26-7
- don't package INSTALL
- define -DLDAP_DEPRECATED=1 in CPPFLAGS

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.26-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.26-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec  5 2005 Joe Orton <jorton@redhat.com> 0.26-6
- link against -lldap and -lcrypto

* Mon Dec  5 2005 Joe Orton <jorton@redhat.com> 0.26-5
- rebuild for httpd 2.2
- fix ssl_var_lookup() use in certmap.c

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 0.26-4
- rebuilt against new openssl

* Fri Mar  4 2005 Joe Orton <jorton@redhat.com> 0.26-3
- rebuild

* Mon Oct  4 2004 Joe Orton <jorton@redhat.com> 0.26-2
- fix auth failures when not configured (#134496)

* Fri Jun 18 2004 Joe Orton <jorton@redhat.com> 0.26-1
- update to 0.26, fix build
- add fix for extern/static conflict

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 21 2004 Joe Orton <jorton@redhat.com> 0.25-1
- update to 0.25

* Fri Sep  5 2003 Joe Orton <jorton@redhat.com> 0.22-3
- don't log the password on auth failure
- obsolete auth_ldap

* Mon Aug  4 2003 Joe Orton <jorton@redhat.com> 0.22-2
- hook up to ssl_var_lookup() in mod_ssl correctly
- include example conf file

* Mon Jun 30 2003 Joe Orton <jorton@redhat.com> 0.22-1
- Initial build.


