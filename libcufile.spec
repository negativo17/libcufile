%global debug_package %{nil}
%global __strip /bin/true
%global _missing_build_ids_terminate_build 0
%global _build_id_links none
%global major_package_version 12-0

Name:           libcufile
Epoch:          1
Version:        1.9.0.20
Release:        1%{?dist}
Summary:        NVIDIA GPUDirect Storage library (cuFile)
License:        CUDA Toolkit
URL:            https://developer.nvidia.com/cuda-toolkit
ExclusiveArch:  aarch64 x86_64

Source0:        https://developer.download.nvidia.com/compute/cuda/redist/%{name}/linux-x86_64/%{name}-linux-x86_64-%{version}-archive.tar.xz
Source1:        https://developer.download.nvidia.com/compute/cuda/redist/%{name}/linux-sbsa/%{name}-linux-sbsa-%{version}-archive.tar.xz
Source2:        cufile.pc

Requires(post): ldconfig
Conflicts:      %{name}-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description
NVIDIA GPUDirect Storage library is used in applications and frameworks to
leverage GDS technology and describes the intent, context, and operation of
those APIs, which are part of the GDS technology.

NVIDIA® Magnum IO GPUDirect® Storage (GDS) is part of the GPUDirect family. GDS
enables a direct data path for direct memory access (DMA) transfers between GPU
memory and storage, which avoids a bounce buffer through the CPU. This direct
path increases system bandwidth and decreases the latency and utilization load
on the CPU.

%package devel
Summary:        Development files for NVIDIA GPUDirect Storage library (cuFile)
Requires:       %{name}%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-devel-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description devel
This package provides development files for the NVIDIA GPUDirect Storage library
(cuFile).

%package static
Summary:        Static libraries for NVIDIA GPUDirect Storage library (cuFile)
Requires:       %{name}-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description static
This package contains static libraries for NVIDIA GPUDirect Storage library
(cuFile).

%package tools
Summary:        NVIDIA GPUDirect Storage library (cuFile) tools and samples
Requires:       %{name}%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       gds-tools-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      gds-tools-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description tools
This package provides tools and samples for the NVIDIA GPUDirect Storage library
(cuFile).

%prep
%ifarch x86_64
%setup -q -n %{name}-linux-x86_64-%{version}-archive
%endif

%ifarch aarch64
%setup -q -T -b 1 -n %{name}-linux-sbsa-%{version}-archive
%endif

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_mandir}
mkdir -p %{buildroot}%{_sysconfdir}

cp -fr tools/gds* %{buildroot}%{_bindir}/
cp -fr include/* %{buildroot}%{_includedir}/
cp -fr lib/lib* %{buildroot}%{_libdir}/
cp -fr %{SOURCE2} %{buildroot}/%{_libdir}/pkgconfig/
cp -fr man/man3 %{buildroot}%{_mandir}/
cp -fr etc/* %{buildroot}%{_sysconfdir}/

# Set proper variables
sed -i \
    -e 's|CUDA_VERSION|%{version}|g' \
    -e 's|LIBDIR|%{_libdir}|g' \
    -e 's|INCLUDE_DIR|%{_includedir}|g' \
    %{buildroot}/%{_libdir}/pkgconfig/*.pc

%{?ldconfig_scriptlets}

%files
%license LICENSE
%doc README
%config %{_sysconfdir}/cufile.json
%{_libdir}/libcufile_rdma.so.*
%{_libdir}/libcufile.so.*

%files devel
%{_includedir}/cufile.h
%{_libdir}/libcufile_rdma.so
%{_libdir}/libcufile.so
%{_libdir}/pkgconfig/cufile.pc
%{_mandir}/man3/CUfileFSOps.3*
%{_mandir}/man3/cufileRDMAInfo.3*
%{_mandir}/man3/cufile.h.3*
%{_mandir}/man3/CUfileDrvProps.3*
%{_mandir}/man3/CUfileDescr_t.3*
%{_mandir}/man3/CUfileError.3*
%{_mandir}/man3/CUfileIOParams.3*
%{_mandir}/man3/CUfileIOEvents.3*
%{_mandir}/man3/CUfileOpError.h.3*

%files static
%{_libdir}/libcufile_rdma_static.a
%{_libdir}/libcufile_static.a

%files tools
%doc tools/README
%doc tools/*.gdsio tools/*.cfg
%{_bindir}/gdscheck
%{_bindir}/gdscheck.py
%{_bindir}/gdscp
%{_bindir}/gdsio
%{_bindir}/gdsio_verify
%{_bindir}/gds_log_collection.py
%{_bindir}/gds_perf.sh
%{_bindir}/gds_stats

%changelog
* Tue Mar 12 2024 Simone Caronni <negativo17@gmail.com> - 1:1.9.0.20-1
- Update to 1.9.0.20.

* Tue Nov 28 2023 Simone Caronni <negativo17@gmail.com> - 1:1.8.1.2-1
- Update to 1.8.1.2.

* Thu Sep 28 2023 Simone Caronni <negativo17@gmail.com> - 1:1.7.2.10-1
- Update to 1.7.2.10.

* Tue Jul 11 2023 Simone Caronni <negativo17@gmail.com> - 1:1.7.0.149-1
- Update to 1.7.0.149.

* Thu Jun 08 2023 Simone Caronni <negativo17@gmail.com> - 1:1.6.1.9-1
- Update to 1.6.1.9.

* Tue Apr 11 2023 Simone Caronni <negativo17@gmail.com> - 1:1.6.0.25-1
- Update to 1.6.0.25.

* Sat Feb 25 2023 Simone Caronni <negativo17@gmail.com> - 1:1.5.1.14-1
- Update to 1.5.1.14.

* Tue Dec 13 2022 Simone Caronni <negativo17@gmail.com> - 1:1.5.0.59-1
- Update to 1.5.0.59.

* Fri Nov 11 2022 Simone Caronni <negativo17@gmail.com> - 1:1.4.0.31-1
- Update to 1.4.0.31.
- Use aarch64 archive in place of sbsa.

* Sun Sep 04 2022 Simone Caronni <negativo17@gmail.com> - 1:1.3.1.18-1
- Update to 1.3.1.18.

* Thu Jun 23 2022 Simone Caronni <negativo17@gmail.com> - 1:1.3.0.44-1
- Update to 1.3.0.44.

* Tue Mar 08 2022 Simone Caronni <negativo17@gmail.com> - 1:1.2.1.4-1
- Update to 1.2.1.4 (CUDA 11.6.1).

* Thu Jan 27 2022 Simone Caronni <negativo17@gmail.com> - 1:1.2.0.100-1
- First build with the new tarball components.
/man/
