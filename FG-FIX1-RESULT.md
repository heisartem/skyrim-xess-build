# XeSS FG lifecycle fix1 — experimental

## Diagnosis and change
The input hook could start a new XeLL frame while render-thread Present was still executing. StartFrameUnlocked completed the previous marker sequence and replaced its ID/tags. This matches the observed unmatched AfterPresent and frame-ID mismatch errors.

BeginFrame now runs in the render hook. IDs follow the actual render/present sequence rather than the global/input counter, and a non-idle sequence cannot be forcibly completed by a new frame start. No logging errors were suppressed.

Pacing now happens later on the render path: input latency and performance must be measured on-device. This is not a complete multi-frame pipelined XeLL redesign. Incorrect-input-resource errors may have independent causes. Shader-cache behavior is unchanged.

## Actual validation
[Windows run 39581698546](https://github.com/heisartem/skyrim-xess-build/actions/runs/39581698546) succeeded.
MSVC 19.51.36260.0, CMake ALL, Release x64. The regression harness compiled actual frame-start methods against mocked SDK calls and passed:
- repeated render hooks preserve the current frame ID;
- a new explicit frame cannot overwrite an in-flight Present or its resource tags;
- the next completed present cycle receives a new ID without dependence on the input/global counter;
- uninitialized context rejects frame start.

Full CommunityShaders.dll compilation/link and package checks passed. This does not simulate the driver or validate Skyrim runtime behavior.

First attempt stopped before compilation due to Windows line endings in the patch/worktree. Normalization resolved it without weakening strict patch-content checks.

## Artifacts
- [MO2 package](https://github.com/heisartem/skyrim-xess-build/actions/runs/39581698546/artifacts/12339183403)
- [Corresponding sources, patch and test](https://github.com/heisartem/skyrim-xess-build/actions/runs/39581698546/artifacts/12338648587)
- [Build/test evidence](https://github.com/heisartem/skyrim-xess-build/actions/runs/39581698546/artifacts/12338798554)

Actual patched source commit: 84fd491fac44d689526a1d8caad69f7e350f27ad.
Base release, PR and XeSS SDK pins are unchanged from BUILD-191-RESULT.md.

Inner ZIP: CommunityShaders-1.9.1-XeSS-FGfix1-MO2.zip
SHA256: 4C60C0998AFBDE8530FBE01DFEB71B3729559901898B61A129133FFBEA99ED98

411 packaged files; complete AIO including 40 feature INIs, shaders and four checked Intel runtime DLLs. Restricted logo omitted. Artifacts expire 2026-11-20.

## Device test
Extract the GitHub outer artifact ZIP and install the inner MO2 ZIP as a separate mod. Disable the previous experimental AIO; prevent standalone CS feature packages from overriding its shaders/configs. Keep the same graphics/HDR/XeSS settings and no competing FG injectors.

Test XeSS FG 2x in the same scene for 2–3 minutes, then open/close the menu several times. Record whether cycling/stutter remains and whether control latency changed. Send the new CommunityShaders.log after exiting the game. Check unmatched AfterPresent, FRAMES_ID_MISMATCH and INCORRECT_INPUT_RESOURCES separately.

Do not delete the shader cache just to test this patch. A rebuild after changing the plugin may occur. Persistence across two unchanged launches is a separate investigation.

XeSS-FG/XeLL on ONEXPLAYER 3 / Arc B390 remain unverified until that test.
