# NOTES
# This spec file is used to build DALi Adaptor for different Tizen Profiles
# Current profiles are:  Mobile, TV, Wearable, Common
#
# The profile variable is defined outside of the spec file in a build.conf file.
# It will contain the profile and whether or not to build with X11 or Wayland
#
# gbs will try to download the build.conf for the platform automatically from the repo location when
# performing a gbs build ( use gbs build -v to see it download location) E.g.
# http://download.tizen.org/snapshots/tizen/tv/tizen-tv/repos/arm-wayland/packages/repodata/xxxx-build.conf.gz

# Do not provide .so automatically for the extensions.
# This if statement is for backward compatibility with GBM/Obsolete build systems
%if "%{?profile}" != "wearable" && "%{?profile}" != "mobile" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
%global __provides_exclude_from ^.*\\.(wearable|mobile|tv|ivi|common)$
%endif

%bcond_with wayland

Name:       dali-adaptor
Summary:    The DALi Tizen Adaptor
Version:    1.2.47
Release:    1
Group:      System/Libraries
License:    Apache-2.0 and BSD-3-Clause and MIT
URL:        https://review.tizen.org/git/?p=platform/core/uifw/dali-adaptor.git;a=summary
Source0:    %{name}-%{version}.tar.gz

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires:       giflib

#need libtzplatform-config for directory if tizen version is 3.x

%if 0%{?tizen_version_major} >= 3
%define tizen_platform_config_supported 1
BuildRequires:  pkgconfig(libtzplatform-config)
%endif

# Get the profile from tizen_profile_name if tizen version is 2.x and tizen_profile_name exists.

%if "%{tizen_version_major}" == "2" && 0%{?tizen_profile_name:1}
%define profile %{tizen_profile_name}
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if wearable || "undefined"
%if "%{?profile}" != "mobile" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
BuildRequires:  pkgconfig(capi-appfw-watch-application)
BuildRequires:  pkgconfig(appcore-watch)
BuildRequires:  pkgconfig(screen_connector_provider)
%endif

BuildRequires:  pkgconfig(gles20)
BuildRequires:  pkgconfig(glesv2)

BuildRequires:  pkgconfig
BuildRequires:  gawk
BuildRequires:  giflib-devel
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  dali-devel
BuildRequires:  dali-integration-devel
BuildRequires:  pkgconfig(vconf)
BuildRequires:  tts-devel
BuildRequires:  pkgconfig(dlog)
BuildRequires:  libdrm-devel
BuildRequires:  pkgconfig(libexif)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(egl)
BuildRequires:  libcurl-devel
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  fribidi-devel

BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(capi-system-sensor)

# Tizen currently does not have libuv as a separate libuv package
# So we have to look into the uv headers bundled inside node-js
BuildRequires:  nodejs-devel


%if %{with wayland}

####### BUILDING FOR WAYLAND #######
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  wayland-devel
BuildRequires:  wayland-extension-client-devel

# dali-adaptor-uv uses libuv mainloop and has its own wayland client (it needs wayland-client headers).
BuildRequires:  libxkbcommon-devel

# dali-adaptor uses ecore mainloop
BuildRequires:  pkgconfig(ecore-wayland)

# dali-adaptor needs tbm_surface in tizen 3.0 wayland
BuildRequires:  pkgconfig(libtbm)

# tpkp-curl (certificate pinning for libcurl functions) is only available in Tizen 3.0
BuildRequires:  pkgconfig(tpkp-curl)

####### BUILDING FOR X11#######
%else
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(utilX)
%endif

# for dali-adaptor
BuildRequires:  pkgconfig(evas)
BuildRequires:  pkgconfig(elementary)

%if 0%{?tizen_version_major} == 3
BuildRequires:  pkgconfig(capi-appfw-application)
%else
BuildRequires:  pkgconfig(appcore-ui)
BuildRequires:  pkgconfig(capi-appfw-app-common)
BuildRequires:  pkgconfig(capi-appfw-app-control)
%endif
BuildRequires:  pkgconfig(capi-system-system-settings)

# for feedback plugin
BuildRequires:  pkgconfig(mm-sound)
%if 0%{?tizen_version_major} >= 3
BuildRequires:  pkgconfig(feedback)
%endif

# for videoplayer Plugin
BuildRequires:  pkgconfig(capi-media-player)


# for multiprofile
Requires:   %{name}-compat = %{version}-%{release}
Recommends: %{name}-profile_common = %{version}-%{release}

%description
The DALi Tizen Adaptor provides a Tizen specific implementation of the dali-core
platform abstraction and application shell

###########################################
# Dali adapter for profiles
###########################################

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if mobile || "undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
%package profile_mobile
Summary:        The DALi Tizen Adaptor for mobile
Provides:       %{name}-compat = %{version}-%{release}
Conflicts:      %{name}-profile_tv
Conflicts:      %{name}-profile_wearable
Conflicts:      %{name}-profile_ivi
Conflicts:      %{name}-profile_common
%description profile_mobile
The DALi Tizen Adaptor for mobile.
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if tv ||"undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "common" && "%{?profile}" != "ivi" && "%{?profile}" != "mobile"
%package profile_tv
Summary:        The DALi Tizen Adaptor for tv
Provides:       %{name}-compat = %{version}-%{release}
Conflicts:      %{name}-profile_mobile
Conflicts:      %{name}-profile_wearable
Conflicts:      %{name}-profile_ivi
Conflicts:      %{name}-profile_common
%description profile_tv
The DALi Tizen Adaptor for tv.
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if wearable || "undefined"
%if "%{?profile}" != "mobile" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
%package profile_wearable
Summary:        The DALi Tizen Adaptor for wearable
Provides:       %{name}-compat = %{version}-%{release}
Conflicts:      %{name}-profile_mobile
Conflicts:      %{name}-profile_tv
Conflicts:      %{name}-profile_ivi
Conflicts:      %{name}-profile_common
%description profile_wearable
The DALi Tizen Adaptor for wearable.
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if ivi ||"undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "common" && "%{?profile}" != "mobile"
%package profile_ivi
Summary:        The DALi Tizen Adaptor for ivi
Provides:       %{name}-compat = %{version}-%{release}
Conflicts:      %{name}-profile_mobile
Conflicts:      %{name}-profile_wearable
Conflicts:      %{name}-profile_tv
Conflicts:      %{name}-profile_common
%description profile_ivi
The DALi Tizen Adaptor for ivi.
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if common ||"undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "mobile"
# Currently Tizen Common we use does not have wayland extensions like xdg-shell
%package profile_common
%define tizen_2_2_compatibility 0
Summary:        The DALi Tizen Adaptor for common
Provides:       %{name}-compat = %{version}-%{release}
Conflicts:      %{name}-profile_mobile
Conflicts:      %{name}-profile_wearable
Conflicts:      %{name}-profile_tv
Conflicts:      %{name}-profile_ivi
%description profile_common
The DALi Tizen Adaptor for common.
%endif

##############################
# devel
##############################
%package devel
Summary:    Development components for the DALi Tizen Adaptor
Group:      Development/Building
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-integration-devel = %{version}-%{release}

%description devel
Development components for the DALi Tizen Adaptor - public headers and package configs

##############################
# integration-devel
##############################
%package integration-devel
Summary:    Integration development package for the Adaptor
Group:      Development/Building
Requires:   %{name} = %{version}-%{release}

%description integration-devel
Integration development package for the Adaptor - headers for integrating with an adaptor library.

##############################
# Dali Feedback Plugin
##############################
%package dali-feedback-plugin
Summary:    Plugin to play haptic and audio feedback for Dali
Group:      System/Libraries
Requires:   %{name} = %{version}-%{release}
%description dali-feedback-plugin
Feedback plugin to play haptic and audio feedback for Dali

##############################
# Dali VideoPlayer Plugin
##############################
%if %{with wayland}

%package dali-video-player-plugin
Summary:    Plugin to play a video file for Dali
Group:      System/Libraries
%description dali-video-player-plugin
VideoPlayer plugin to play a video file for Dali
%endif

##############################
# Preparation
##############################
%prep
%setup -q

#Use TZ_PATH when tizen version is 3.x or greater

%if 0%{?tizen_version_major} >= 3
%define dali_data_rw_dir         %TZ_SYS_RO_SHARE/dali/
%define dali_data_ro_dir         %TZ_SYS_RO_SHARE/dali/
%define font_preloaded_path      %TZ_SYS_RO_SHARE/fonts/
%define font_downloaded_path     %TZ_SYS_SHARE/fonts/
%define font_application_path    %TZ_SYS_RO_SHARE/app_fonts/
%define font_configuration_file  %TZ_SYS_ETC/fonts/conf.avail/99-slp.conf
%else
%define dali_data_rw_dir         /usr/share/dali/
%define dali_data_ro_dir         /usr/share/dali/
%define font_preloaded_path      /usr/share/fonts/
%define font_downloaded_path     /opt/share/fonts/
%define font_application_path    /usr/share/app_fonts/
%define font_configuration_file  /opt/etc/fonts/conf.avail/99-slp.conf
%endif

%define user_shader_cache_dir    %{dali_data_ro_dir}/core/shaderbin/
%define dali_plugin_sound_files  /plugins/sounds/
%define dev_include_path %{_includedir}

##############################
# Build
##############################
%build
PREFIX+="/usr"
CXXFLAGS+=" -Wall -g -Os -fPIC -fvisibility-inlines-hidden -fdata-sections -ffunction-sections -DGL_GLEXT_PROTOTYPES"
LDFLAGS+=" -Wl,--rpath=%{_libdir} -Wl,--as-needed -Wl,--gc-sections -Wl,-Bsymbolic-functions "

%ifarch %{arm}
CXXFLAGS+=" -D_ARCH_ARM_ -lgcc"
%endif

%if %{with wayland}
CFLAGS+=" -DWAYLAND"
CXXFLAGS+=" -DWAYLAND"
configure_flags="--enable-wayland"
%endif

# Use this conditional when Tizen version is 4.x or greater
%if 0%{?tizen_version_major} >= 4
CXXFLAGS+=" -DOVER_TIZEN_VERSION_4"
%endif

%if 0%{?tizen_2_2_compatibility}
CFLAGS+=" -DTIZEN_SDK_2_2_COMPATIBILITY"
CXXFLAGS+=" -DTIZEN_SDK_2_2_COMPATIBILITY"
%endif

libtoolize --force
cd %{_builddir}/%{name}-%{version}/build/tizen
autoreconf --install

DALI_DATA_RW_DIR="%{dali_data_rw_dir}" ; export DALI_DATA_RW_DIR
DALI_DATA_RO_DIR="%{dali_data_ro_dir}"  ; export DALI_DATA_RO_DIR
FONT_PRELOADED_PATH="%{font_preloaded_path}" ; export FONT_PRELOADED_PATH
FONT_DOWNLOADED_PATH="%{font_downloaded_path}" ; export FONT_DOWNLOADED_PATH
FONT_APPLICATION_PATH="%{font_application_path}"  ; export FONT_APPLICATION_PATH
FONT_CONFIGURATION_FILE="%{font_configuration_file}" ; export FONT_CONFIGURATION_FILE
%if 0%{?tizen_platform_config_supported}
TIZEN_PLATFORM_CONFIG_SUPPORTED="%{tizen_platform_config_supported}" ; export TIZEN_PLATFORM_CONFIG_SUPPORTED
%endif

# Default to GLES 2.0 if not specified.
%{!?target_gles_version: %define target_gles_version 20}

#--enable-efl=no \ # only affects dali-adaptor-uv
#--enable-appfw=yes \ # affects both dali-adaptor & dali-adaptor-uv
#--with-libuv=/usr/include/node/ \ # only affects dali-adaptor-uv


# Set up the build via configure.
#######################################################################
# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if mobile || "undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
%configure --prefix=$PREFIX --with-jpeg-turbo --enable-gles=%{target_gles_version} \
           --enable-shaderbincache=DISABLE --enable-profile=MOBILE \
           --enable-tizen-major-version=%{tizen_version_major} \
%if 0%{?tizen_version_major} >= 3
           --enable-feedback \
%endif
           --enable-videoplayer \
%if 0%{?tizen_2_2_compatibility}
           --with-tizen-2-2-compatibility \
%endif
%if %{with wayland}
           --enable-efl=no \
%else
           --enable-efl=yes \
%endif
%if 0%{?enable_debug}
           --enable-debug \
%endif
           --enable-appfw=yes \
           --with-libuv=/usr/include/node/ \
           $configure_flags --libdir=%{_libdir}

# Build.
make %{?jobs:-j%jobs}

pushd %{_builddir}/%{name}-%{version}/build/tizen
%make_install DALI_DATA_RW_DIR="%{dali_data_rw_dir}" DALI_DATA_RO_DIR="%{dali_data_ro_dir}"
popd

pushd %{buildroot}%{_libdir}
for FILE in libdali-adap*.so*; do mv "$FILE" "%{_builddir}/%{name}-%{version}/build/tizen/$FILE.mobile"; done
popd

%endif

#######################################################################
# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if tv ||"undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "common" && "%{?profile}" != "ivi" && "%{?profile}" != "mobile"
%configure --prefix=$PREFIX --with-jpeg-turbo --enable-gles=%{target_gles_version} \
           --enable-shaderbincache=DISABLE --enable-profile=TV \
           --enable-tizen-major-version=%{tizen_version_major} \
%if 0%{?tizen_version_major} >= 3
           --enable-feedback \
%endif
           --enable-videoplayer \
%if 0%{?tizen_2_2_compatibility}
           --with-tizen-2-2-compatibility \
%endif
%if %{with wayland}
           --enable-efl=no \
%else
           --enable-efl=yes \
%endif
%if 0%{?enable_debug}
           --enable-debug \
%endif
           --enable-appfw=yes \
           --with-libuv=/usr/include/node/ \
           $configure_flags --libdir=%{_libdir}

# Build.
make %{?jobs:-j%jobs}

pushd %{_builddir}/%{name}-%{version}/build/tizen
%make_install DALI_DATA_RW_DIR="%{dali_data_rw_dir}" DALI_DATA_RO_DIR="%{dali_data_ro_dir}"
popd

pushd %{buildroot}%{_libdir}
for FILE in libdali-adap*.so*; do mv "$FILE" "%{_builddir}/%{name}-%{version}/build/tizen/$FILE.tv"; done
popd

%endif

#######################################################################
# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if wearable || "undefined"
%if "%{?profile}" != "mobile" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
%configure --prefix=$PREFIX --with-jpeg-turbo --enable-gles=%{target_gles_version} \
           --enable-shaderbincache=DISABLE --enable-profile=WEARABLE \
           --enable-tizen-major-version=%{tizen_version_major} \
%if 0%{?tizen_version_major} >= 3
           --enable-feedback \
%endif
           --enable-videoplayer \
%if 0%{?tizen_2_2_compatibility}
           --with-tizen-2-2-compatibility \
%endif
%if %{with wayland}
           --enable-efl=no \
%else
           --enable-efl=yes \
%endif
%if 0%{?enable_debug}
           --enable-debug \
%endif
           --enable-appfw=yes \
           --with-libuv=/usr/include/node/ \
           $configure_flags --libdir=%{_libdir}

# Build.
make %{?jobs:-j%jobs}

pushd %{_builddir}/%{name}-%{version}/build/tizen
%make_install DALI_DATA_RW_DIR="%{dali_data_rw_dir}" DALI_DATA_RO_DIR="%{dali_data_ro_dir}"
popd

pushd %{buildroot}%{_libdir}
for FILE in libdali-adap*.so*; do mv "$FILE" "%{_builddir}/%{name}-%{version}/build/tizen/$FILE.wearable"; done
popd

%endif

#######################################################################
# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if ivi ||"undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "common" && "%{?profile}" != "mobile"
%configure --prefix=$PREFIX --with-jpeg-turbo --enable-gles=%{target_gles_version} \
           --enable-shaderbincache=DISABLE --enable-profile=IVI \
           --enable-tizen-major-version=%{tizen_version_major} \
%if 0%{?tizen_version_major} >= 3
           --enable-feedback \
%endif
           --enable-videoplayer \
%if 0%{?tizen_2_2_compatibility}
           --with-tizen-2-2-compatibility \
%endif
%if %{with wayland}
           --enable-efl=no \
%else
           --enable-efl=yes \
%endif
%if 0%{?enable_debug}
           --enable-debug \
%endif
           --enable-appfw=yes \
           --with-libuv=/usr/include/node/ \
           $configure_flags --libdir=%{_libdir}

# Build.
make %{?jobs:-j%jobs}

pushd %{_builddir}/%{name}-%{version}/build/tizen
%make_install DALI_DATA_RW_DIR="%{dali_data_rw_dir}" DALI_DATA_RO_DIR="%{dali_data_ro_dir}"
popd

pushd %{buildroot}%{_libdir}
for FILE in libdali-adap*.so*; do mv "$FILE" "%{_builddir}/%{name}-%{version}/build/tizen/$FILE.ivi"; done
popd

%endif

#######################################################################
# common ( build dali_videoplayer_plugin for common uses )
# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if common ||"undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "mobile"
%configure --prefix=$PREFIX --with-jpeg-turbo --enable-gles=%{target_gles_version} \
           --enable-shaderbincache=DISABLE --enable-profile=COMMON \
           --enable-tizen-major-version=%{tizen_version_major} \
%if 0%{?tizen_version_major} >= 3
           --enable-feedback \
%endif
           --enable-videoplayer \
%if 0%{?tizen_2_2_compatibility}
           --with-tizen-2-2-compatibility \
%endif
%if %{with wayland}
           --enable-efl=no \
%else
           --enable-efl=yes \
%endif
%if 0%{?enable_debug}
           --enable-debug \
%endif
           --enable-appfw=yes \
           --with-libuv=/usr/include/node/ \
           $configure_flags --libdir=%{_libdir}

# Build.
make %{?jobs:-j%jobs}
%endif


##############################
# Installation
##############################
%install
rm -rf %{buildroot}

pushd %{_builddir}/%{name}-%{version}/build/tizen
%make_install DALI_DATA_RW_DIR="%{dali_data_rw_dir}" DALI_DATA_RO_DIR="%{dali_data_ro_dir}"


# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# !unified && (wearable || tv || ivi || mobile)
%if "%{?profile}" == "wearable" || "%{?profile}" == "tv" || "%{?profile}" == "ivi" || "%{?profile}" == "mobile"
rm -rf %{buildroot}%{_libdir}/libdali-adap*.so*
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# wearable || tv || ivi || mobile || unified
%if "%{?profile}" != "common"
for FILE in libdali-*.so*; do mv "$FILE" "%{buildroot}%{_libdir}/$FILE"; done
%endif
popd

##############################
# Upgrade order:
# 1 - Pre Install new package
# 2 - Install new package
# 3 - Post install new package
# 4 - Pre uninstall old package
# 5 - Remove files not overwritten by new package
# 6 - Post uninstall old package
##############################

%pre
exit 0

##############################
#  Post Install new package
##############################
%post
/sbin/ldconfig
exit 0

##############################
#  Pre Uninstall old package
##############################
%preun
exit 0

##############################
#  Post Uninstall old package
##############################
%postun
/sbin/ldconfig
exit 0

%if %{with wayland}
%post dali-video-player-plugin
/sbin/ldconfig
exit 0
%endif

%if %{with wayland}
%postun dali-video-player-plugin
/sbin/ldconfig
exit 0
%endif


##############################

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if mobile || "undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
%post profile_mobile
pushd %{_libdir}
for FILE in libdali-adap*.so*.mobile; do ln -sf "$FILE" "${FILE%.mobile}"; done
popd
/sbin/ldconfig
exit 0

%postun profile_mobile
/sbin/ldconfig
exit 0
%endif

##############################

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if tv ||"undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "common" && "%{?profile}" != "ivi" && "%{?profile}" != "mobile"
%post profile_tv
pushd %{_libdir}
for FILE in libdali-adap*.so*.tv; do ln -sf "$FILE" "${FILE%.tv}"; done
popd
/sbin/ldconfig
exit 0

%postun profile_tv
/sbin/ldconfig
exit 0
%endif

##############################

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if wearable || "undefined"
%if "%{?profile}" != "mobile" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
%post profile_wearable
pushd %{_libdir}
for FILE in libdali-adap*.so*.wearable; do ln -sf "$FILE" "${FILE%.wearable}"; done
popd
/sbin/ldconfig
exit 0

%postun profile_wearable
/sbin/ldconfig
exit 0
%endif

##############################

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if ivi ||"undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "common" && "%{?profile}" != "mobile"
%post profile_ivi
pushd %{_libdir}
for FILE in libdali-adap*.so*.ivi; do ln -sf "$FILE" "${FILE%.ivi}"; done
popd
/sbin/ldconfig
exit 0

%postun profile_ivi
/sbin/ldconfig
exit 0
%endif


##############################
# Files in Binary Packages
##############################

%files
%manifest dali-adaptor.manifest
%defattr(-,root,root,-)
%defattr(-,app,app,-)
%dir %{user_shader_cache_dir}
%{_bindir}/*
%license LICENSE

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if common ||"undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "mobile"
%defattr(-,root,root,-)
%{_libdir}/libdali-adap*.so*
%exclude %{_libdir}/libdali-adap*.so*.mobile
%exclude %{_libdir}/libdali-adap*.so*.wearable
%exclude %{_libdir}/libdali-adap*.so*.tv
%exclude %{_libdir}/libdali-adap*.so*.ivi
%endif

%if %{with wayland}
%files dali-video-player-plugin
%manifest dali-adaptor.manifest
%defattr(-,root,root,-)
%{_libdir}/libdali-video-player-plugin.so*
%license LICENSE
%endif

%if 0%{?tizen_version_major} >= 3
%files dali-feedback-plugin
%manifest dali-adaptor.manifest
%defattr(-,root,root,-)
%{_libdir}/libdali-feedback-plugin.so*
%{dali_plugin_sound_files}/*
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if common ||"undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "mobile"
%files profile_common
# default .so files are housed in the main pkg.
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if mobile || "undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
%files profile_mobile
%manifest dali-adaptor.manifest
%defattr(-,root,root,-)
%{_libdir}/libdali-adap*.so*.mobile
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if tv ||"undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "common" && "%{?profile}" != "ivi" && "%{?profile}" != "mobile"
%files profile_tv
%manifest dali-adaptor.manifest
%defattr(-,root,root,-)
%{_libdir}/libdali-adap*.so*.tv
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if wearable || "undefined"
%if "%{?profile}" != "mobile" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
%files profile_wearable
%manifest dali-adaptor.manifest
%defattr(-,root,root,-)
%{_libdir}/libdali-adap*.so*.wearable
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if ivi ||"undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "common" && "%{?profile}" != "mobile"
%files profile_ivi
%manifest dali-adaptor.manifest
%defattr(-,root,root,-)
%{_libdir}/libdali-adap*.so*.ivi
%endif


%files devel
%defattr(-,root,root,-)
%{dev_include_path}/dali/dali.h
%{dev_include_path}/dali/public-api/*
%{dev_include_path}/dali/devel-api/*
%{dev_include_path}/dali/doc/*
%{_libdir}/pkgconfig/dali-adaptor.pc
%{_libdir}/pkgconfig/dali-adaptor-uv.pc

%files integration-devel
%defattr(-,root,root,-)
%{dev_include_path}/dali/integration-api/adaptors/*
%{_libdir}/pkgconfig/dali-adaptor-integration.pc
