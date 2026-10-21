"""Merge the original XeSS PR into the pinned CS 1.9.1 release.
Run inside a disposable checkout of upstream CS. Does not push any refs.
Original XeSS authorship: NightHammer1000, upstream PR #2704.
"""
import json
import pathlib
import subprocess

RELEASE = "265c28f53767e94dac1c0c3b211a0aa37d8ec396"
PR = "9cd53ce033a2817ddfc66aa627b63fc62872600c"
BASE = "09ea74f66e12bad462b9ae4f16a9f6cacc02993d"

def git(*args, check=True):
    return subprocess.run(["git", *args], check=check, capture_output=True, text=True)

assert git("rev-parse", "HEAD").stdout.strip() == RELEASE, "Unexpected release checkout"
git("fetch", "--no-tags", "https://github.com/NightHammer1000/skyrim-community-shaders.git", PR)
assert git("merge-base", RELEASE, PR).stdout.strip() == BASE, "Unexpected merge base"
git("config", "user.name", "XeSS experimental build")
git("config", "user.email", "86159606+heisartem@users.noreply.github.com")
result = git("merge", "--no-ff", "--no-commit", PR, check=False)
conflicts = set(git("diff", "--name-only", "--diff-filter=U").stdout.splitlines())
expected = {
    "features/HDR Display/Shaders/Features/HDRDisplay.ini",
    "src/Features/Upscaling.cpp",
}
assert result.returncode == 1 and conflicts == expected, (
    "Unexpected merge outcome", result.stdout, result.stderr, conflicts
)

for name in sorted(conflicts):
    path = pathlib.Path(name)
    text = path.read_text(encoding="utf-8")
    assert text.count("<<<<<<<") == 1 and text.count("=======") == 1 and text.count(">>>>>>>") == 1
    prefix, rest = text.split("<<<<<<<", 1)
    _, rest = rest.split("\n", 1)
    ours, rest = rest.split("=======\n", 1)
    theirs, rest = rest.split(">>>>>>>", 1)
    _, suffix = rest.split("\n", 1)
    if name.endswith(".ini"):
        assert ours.strip() == "Version = 1-2-2"
        assert theirs.strip() == "Version = 1-3-0"
        replacement = theirs
    else:
        assert "settings.qualityMode > 4" in ours
        assert "settings.frameGenerationMode >" in theirs
        assert "clampedMultiplier" in theirs and "frameGenerationXeSSUIMode" in theirs
        # Both sides use the same final closing brace in the common suffix.
        # Close the quality-mode check before preserving all XeSS checks.
        replacement = ours + "\t}\n" + theirs
    path.write_text(prefix + replacement + suffix, encoding="utf-8", newline="\n")
    git("add", "--", name)

assert not git("diff", "--name-only", "--diff-filter=U").stdout.strip()
git("diff", "--cached", "--check")
for lang in ("en", "ru", "zh_CN"):
    json.loads(pathlib.Path("package/SKSE/Plugins/CommunityShaders/Translations/" + lang + ".json").read_text(encoding="utf-8"))
up = pathlib.Path("src/Features/Upscaling.cpp").read_text(encoding="utf-8")
assert "settings.qualityMode > 4" in up and "settings.frameGenerationMode >" in up
assert "detour_thunk<SetScissorRect>" not in up, "Do not restore obsolete DRS hook"
hdr = pathlib.Path("src/Features/HDRDisplay.cpp").read_text(encoding="utf-8")
assert "RestoreCleanScene();" in hdr
assert "loaded && settings.enableHDR && hdrDataCB && outputTexture" in hdr
assert "VERSION 1.9.1" in pathlib.Path("CMakeLists.txt").read_text(encoding="utf-8")
git("commit", "-m", "Merge NightHammer1000 XeSS PR #2704 into CS v1.9.1; preserve release fixes")
git("submodule", "sync", "--recursive")
git("submodule", "update", "--init", "--recursive")
sdk = git("-C", "extern/XeSS-SDK", "rev-parse", "HEAD").stdout.strip()
assert sdk == "8fe81bdbbaf00b3c1b733fd0d830c333dc84e6f0"
print(json.dumps({"release": RELEASE, "original_pr": PR, "merge": git("rev-parse", "HEAD").stdout.strip(), "sdk": sdk, "conflicts_resolved": sorted(conflicts)}))
