# Unofficial XeSS port to CS 1.9.1

Original integration by NightHammer1000: community-shaders/skyrim-community-shaders#2704.
This branch records the reproducible port recipe; it is not a GitHub fork or a full mirror of upstream source history.

Pinned release: 265c28f53767e94dac1c0c3b211a0aa37d8ec396.
Pinned PR: 9cd53ce033a2817ddfc66aa627b63fc62872600c.
merge-xess.py performs a real Git merge in a disposable upstream checkout and refuses unexpected conflicts.
It preserves both quality and XeSS FG setting validation, HDRDisplay 1.3.0, release HDR fixes, and the release's moved DRS scissor handling.
Full source and original author history remain in that checkout; no push to upstream occurs.

## Device feedback on the ORIGINAL PR build
- Skyrim starts on ONEXPLAYER 3 / Arc B390.
- User reports shader compilation on every launch.
- User reports worse frame-generation performance than their PureDark configuration.
- Earlier screenshot showed HDRDisplay feature-version mismatch; packaged INI was verified as 1-3-0.

None of these runtime issues is diagnosed or fixed by the merge recipe.
Required evidence: CommunityShaders.log from two consecutive unchanged runs, Data/ShaderCache/Info.ini as seen through MO2, Upscaling settings, same-scene FG off/on FPS and frametimes, Intel driver version, resolution, refresh rate, power limit and identical enabled CS features.
A startup progress bar alone does not prove disk-cache loss.
The original source logs cache validation and XeSS-FG/XeLL initialization/errors.

## Validation status
Draft port. Source-merge validation is separate from MSVC compilation and on-device validation.
Do not describe this branch as a working 1.9.1 binary until its own Windows build succeeds.
Keep the known original PR archive and test profile separate.

## Licensing
Upstream code retains GPL-3.0-or-later and upstream exceptions/copyright notices.
XeSS binaries retain Intel's license and third-party notices.
The CS logo has separate personal-use restrictions. This validation workflow publishes no binaries, logos or full source archive.
Any future downloadable package must preserve required notices and provide corresponding source, while excluding restricted branding or obtaining permission.
