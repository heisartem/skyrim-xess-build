# Experimental CS 1.9.1 + XeSS: successful Windows build

Run: https://github.com/heisartem/skyrim-xess-build/actions/runs/39568766887
Windows-2025, MSVC, CMake ALL / Release / x64. Compilation, installation, package validation and artifact uploads succeeded on 2026-10-21.

## Provenance
- Release: 265c28f53767e94dac1c0c3b211a0aa37d8ec396.
- Original NightHammer1000 PR #2704: 9cd53ce033a2817ddfc66aa627b63fc62872600c.
- Actual merged source: d3af32c3b3e4277d2e1a6f58b9fd0740c33fc8bd.
- XeSS SDK v3.0.2: 8fe81bdbbaf00b3c1b733fd0d830c333dc84e6f0.
- No current dev merge and no additional compiler fixes were needed.
- Two merge conflicts resolved by the checked-in recipe: HDRDisplay feature version and adjacent Upscaling settings validation.

## Downloads
- [MO2 package](https://github.com/heisartem/skyrim-xess-build/actions/runs/39568766887/artifacts/12331862549)
- [Merged sources including recursive submodules and build recipe](https://github.com/heisartem/skyrim-xess-build/actions/runs/39568766887/artifacts/12331728420)
- [Build evidence, manifest and logs](https://github.com/heisartem/skyrim-xess-build/actions/runs/39568766887/artifacts/12331433973)

GitHub downloads an outer artifact ZIP. Extract it and install the inner `CommunityShaders-1.9.1-XeSS-PR2704-MO2.zip` in MO2.

Inner ZIP SHA256:
`D6F78D292E0334A1D99B2C7ECC0F05D61262F04BBC9FC3861DEF16F3F05BFDBA`

Artifacts currently expire on 2026-11-20; download and retain them together.

## Validated
- Build log contains IntelXeSS.cpp, IntelXeSSD3D12.cpp and IntelXeSSFrameGeneration.cpp compilation and CommunityShaders.dll output.
- Plugin is an x64 PE DLL; imports recorded.
- 40 feature INIs, HLSL shaders and all four Intel runtime DLLs are packaged.
- Intel runtime hashes match the pinned SDK.
- ZIP root is the contents of Skyrim Data, with SKSE/Plugins and Shaders.
- Restricted upstream logo omitted; source and license notices included.
- No claim of a complete legal audit.

## Install and test
Use a separate MO2 test profile. Disable the previous CS core/AIO and overlapping standalone CS feature packages. This AIO includes Upscaling and HDR Display; its shaders and feature INIs must not be overwritten by older versions. Disable other competing upscaling/frame-generation injectors for this test. Keep the normal SKSE, Address Library and runtime prerequisites.

Allow initial shader compilation. Start with FG off, then test XeSS FG 2x in the same scene with identical resolution, power limit and enabled CS features.

This merged binary has NOT been tested in Skyrim on ONEXPLAYER 3 / Intel Arc B390. XeSS-FG/XeLL require device testing. The original build's repeated shader startup compilation and poorer FG performance are not claimed fixed.

The previous original PR build remains available separately. Draft PR #1 is intentionally not merged into main pending device testing.
