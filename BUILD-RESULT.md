# Successful original PR build

[Run 39499136543](https://github.com/heisartem/skyrim-xess-build/actions/runs/39499136543) completed successfully.
Source commit: `9cd53ce033a2817ddfc66aa627b63fc62872600c`.
Compiler: MSVC 19.51.36260.0; CMake ALL Release; Windows runner.
No source patches or dev/1.9.1 merge were needed.

The log records compilation of IntelXeSS.cpp, IntelXeSSD3D12.cpp and IntelXeSSFrameGeneration.cpp, and creation of build/ALL/Release/CommunityShaders.dll.
The runner verified recursive submodules, XeSS SDK v3.0.2 and SHA-256 equality of all four packaged XeSS DLLs with SDK binaries.
CMake installation, x64 PE check and ZIP layout/file-count checks passed.

- [Download artifact containing the MO2 ZIP](https://github.com/heisartem/skyrim-xess-build/actions/runs/39499136543/artifacts/12302765269) — approximately 181 MB.
- [Download logs, manifests and checksums](https://github.com/heisartem/skyrim-xess-build/actions/runs/39499136543/artifacts/12303135136).
- Extract the outer GitHub artifact ZIP, then install the inner CommunityShaders-XeSS-PR2704-9cd53ce-MO2.zip in MO2.
- Artifacts have a 30-day retention period. Download a local copy.

The inner ZIP has SKSE and Shaders at its root, including SKSE/Plugins/CommunityShaders.dll and Shaders/Upscaling/XeSS/{libxess.dll,libxess_dx11.dll,libxess_fg.dll,libxell.dll}.
It includes the complete original AIO feature content and original settings, not a separate plugin for CS 1.9.1.

External prerequisites are not bundled: Skyrim, matching SKSE and Address Library, Intel graphics driver, and a compatible x64 Microsoft Visual C++ runtime. The plugin imports MSVCP140.dll, MSVCP140_ATOMIC_WAIT.dll, VCRUNTIME140.dll and VCRUNTIME140_1.dll.

Use a copied MO2 profile and disable the previous CS 1.9.1 and overlapping standalone CS feature packages, including Upscaling. See README.md for installation.

## Not yet validated
Skyrim startup, runtime shader compilation, image quality, performance, XeSS-FG and XeLL on ONEXPLAYER 3 / Arc B390.
Test XeSS-SR first with FG off, then XeSS-FG at 2x in SDR. Device testing is mandatory before treating this as a working hardware configuration. HDR needs a separate test.
Only after the original PR device test should a separate 1.9.1 port be considered.
