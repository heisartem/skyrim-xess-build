# Skyrim Community Shaders — experimental Intel XeSS build

Build harness for [PR #2704](https://github.com/community-shaders/skyrim-community-shaders/pull/2704).
This repository does not replace the integration with a separate upscaling mod.

## Source and status

- Source: NightHammer1000/skyrim-community-shaders
- Exact PR head: `9cd53ce033a2817ddfc66aa627b63fc62872600c`
- XeSS SDK v3.0.2: `8fe81bdbbaf00b3c1b733fd0d830c333dc84e6f0`
- Recursive submodules, original CMake ALL Release preset, MSVC on windows-2025.
- No merge with current dev and no source patches in the initial attempt.
- Check the actual Actions run and build logs for status. A workflow file is not proof of compilation.
- Target device: ONEXPLAYER 3 / Intel Arc B390. No device testing has been performed.

The workflow compares all four bundled XeSS DLLs with the pinned SDK, compiles CommunityShaders, runs the original CMake AIO installation, checks required files and the x64 plugin, and creates a ZIP whose root is Skyrim's Data directory content. It also records file hashes and compiler logs.

## Download after a successful build

Open Actions → Build original XeSS PR for MO2 → a successful run.
Download the `CommunityShaders-XeSS-MO2` artifact. Extract GitHub's outer artifact archive; the inner `CommunityShaders-XeSS-PR2704-9cd53ce-MO2.zip` is the MO2 installer archive.
Download `build-evidence` separately for logs, source/submodule provenance, the package manifest and ZIP SHA-256.

An absent artifact or a failed job is not a usable build.

## Installation in MO2

1. Use a separate MO2 test profile. Back up your existing Community Shaders settings.
2. Install SKSE for your exact Skyrim executable version and the matching Address Library for SSE/AE. These external prerequisites are not included in this mod archive.
3. Disable your existing Community Shaders package and its separately installed feature packages for this test so older DLLs, shaders or feature INI files do not overwrite the experimental AIO.
4. Install the inner MO2 ZIP using Install a new mod from an archive. The archive root should contain `SKSE` and `Shaders` directly; it must not be nested under an extra project folder.
5. Launch SKSE through MO2. Allow runtime shader compilation to finish.
6. Start by testing XeSS Super Resolution with frame generation off. Then test XeSS Frame Generation separately. Preserve the settings files from this build; do not replace its Upscaling or HDR shaders with those from another release.

The original feature metadata is Upscaling 1-5-0 and HDRDisplay 1-3-0. This AIO includes the source project's feature content; it is not a performance-tuned preset for the handheld.

## Hardware testing still required

Successful MSVC compilation and archive validation do not establish in-game compatibility.
XeSS-FG and XeLL must be tested on the actual ONEXPLAYER 3 / Arc B390, including menu-to-game transitions, input responsiveness, UI flicker, frame pacing, resizing/alt-tab and stability.
Test SDR first; HDR requires a separate pass. Record the Intel driver version, Skyrim runtime, resolution, SR quality, FG multiplier and logs.

## Licensing and source

The compiled code and third-party components retain their upstream licenses.
See the pinned source repository's COPYING, EXCEPTIONS.md, per-component licenses and XeSS SDK license.
This harness does not publish a GitHub Release; artifacts are intended for the requested personal experimental build.
