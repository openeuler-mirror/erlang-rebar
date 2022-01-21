%global realname rebar
%global upstream rebar
%global need_bootstrap_set 0
%{!?need_bootstrap: %global need_bootstrap  %{need_bootstrap_set}}
Name:		erlang-%{realname}
Version:	2.6.4
Release:	2
BuildArch:	noarch
Summary:	Erlang Build Tools
License:	MIT
URL:		https://github.com/%{upstream}/%{realname}
Source0:	https://github.com/%{upstream}/%{realname}/archive/%{version}/%{realname}-%{version}.tar.gz
Patch1:		rebar-0001-Load-templates-from-the-filesystem-first.patch
Patch2:		rebar-0002-Remove-bundled-mustache.patch
Patch3:		rebar-0003-Remove-bundled-getopt.patch
Patch4:		rebar-0004-Allow-discarding-building-ports.patch
Patch5:		rebar-0005-Remove-any-traces-of-long-time-obsolete-escript-fold.patch
Patch6:		rebar-0006-remove-abnfc.patch
Patch7:		rebar-0007-Remove-support-for-gpb-compiler.patch
Patch8:		rebar-0008-Remove-pre-R15B02-workaround.patch
Patch9:		rebar-0009-Use-erlang-timestamp-0-explicitly.patch
Patch10:	rebar-0010-Try-shell-variable-VSN-first.patch
Patch11:	rebar-0011-Allow-ignoring-missing-deps.patch
Patch12:	rebar-0012-Drop-obsolete-crypto-rand_uniform-2.patch
Patch13:	rebar-0013-Remove-compat-random-modules.patch
Patch14:        0014-remove-lerl_interface-build-flag.patch
%if 0%{?need_bootstrap} < 1
BuildRequires:       	erlang-rebar 	erlang-getopt
%else
BuildRequires:       	erlang-asn1 	erlang-common_test 	erlang-compiler 	erlang-crypto
BuildRequires:       	erlang-dialyzer 	erlang-diameter 	erlang-edoc 	erlang-eflame
BuildRequires:       	erlang-erl_interface 	erlang-erlydtl 	erlang-erts 	erlang-eunit 	erlang-getopt
BuildRequires:       	erlang-kernel 	erlang-lfe 	erlang-mustache 	erlang-neotoma 	erlang-parsetools
BuildRequires:       	erlang-protobuffs 	erlang-reltool 	erlang-rpm-macros 	erlang-sasl 	erlang-snmp
BuildRequires:       	erlang-stdlib 	erlang-syntax_tools 	erlang-tools 	erlang-triq
%endif
Requires:            	erlang-common_test 	erlang-erl_interface 	erlang-parsetools
Requires:            	erlang-rpm-macros >= 0.2.4
Provides:	%{realname} = %{version}-%{release}
%description
Erlang Build Tools.

%prep
%setup -q -n %{realname}-%{version}
touch ./rebar.escript
cat <<EOT >>./rebar.escript
#!/usr/bin/env escript
%%%%! -noshell -noinput

main (Args) ->
	rebar:main(Args).
EOT
%patch1 -p1 -b .load_templates_from_fs
%patch2 -p1 -b .remove_bundled_mustache
%if 0%{?need_bootstrap} < 1
%patch3 -p1 -b .remove_bundled_getopt
%endif
%patch4 -p1 -b .allow_discarding_ports
%patch5 -p1 -b .remove_escript_foldl_3
%patch6 -p1 -b .remove_abnfc
%patch7 -p1 -b .remove_gpb
%patch8 -p1 -b .remove_pre_R15B02
%patch9 -p1 -b .erlang_timestamp_0
%patch10 -p1 -b .vsn_override
%patch11 -p1 -b .skip_deps_checking
%patch12 -p1 -b .erl20
%patch13 -p1 -b .erl22_compat
%patch14 -p1

%build
%if 0%{?need_bootstrap} < 1
%{erlang_compile}
%else
./bootstrap
./rebar compile -v
%endif

%install
%{erlang_install}
install -D -p -m 0755 %{_builddir}/%{realname}-%{version}/rebar.escript %{buildroot}%{_bindir}/rebar
cp -a priv %{buildroot}%{_erllibdir}/%{realname}-%{version}/

%check
%if 0%{?need_bootstrap} < 1
install -D -p -m 0755 %{_builddir}/%{realname}-%{version}/rebar.escript ./rebar
sed -i -e "s,-noshell -noinput,-noshell -noinput -pa .,g" ./rebar
%{rebar_eunit}
%endif

%files
%doc README.md THANKS rebar.config.sample
%license LICENSE
%{_bindir}/rebar
%{erlang_appdir}/

%changelog
* Fri Jan 21 2022 Ge Wang <wangge20huawei.com> - 2.6.4-2
- Remove -lerl_interface flag from default LDFLAG due to erlang updated to 23.3.4.9 version

* Fri Sep 4 2020 Ge Wang <wangge20@huawei.com> - 2.6.4-1
- Package init
