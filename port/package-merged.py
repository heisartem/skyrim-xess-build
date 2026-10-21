"""Preserve corresponding merged sources, notices and reproducible build recipe."""
import os, pathlib, subprocess, zipfile, shutil
root = pathlib.Path.cwd()
stage = pathlib.Path(os.environ["MO2_STAGE"])
logo = pathlib.Path("Interface/CommunityShaders/Icons/Community Shaders Logo")
shutil.rmtree(stage / logo, ignore_errors=True)
docs = stage / "CommunityShaders-XeSS-Build"
docs.mkdir(exist_ok=True)
def tracked(repo):
    data = subprocess.check_output(["git", "-C", str(repo), "ls-files", "--stage", "-z"])
    for record in data.split(b"\0"):
        if not record:
            continue
        meta, name = record.split(b"\t", 1)
        mode = meta.split()[0]
        rel = pathlib.Path(os.fsdecode(name))
        if mode == b"160000":
            yield from tracked(repo / rel)
        else:
            path = repo / rel
            if path.is_file() and "Community Shaders Logo" not in path.parts:
                yield path
files = list(tracked(root))
for path in files:
    if any(t in path.name.lower() for t in ("license", "copying", "exception", "notice")):
        dest = docs / "licenses" / path.relative_to(root)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
for name in ("merge-xess.py", "README.md", "package-merged.py"):
    shutil.copy2(root / "_harness" / "port" / name, docs / name)
shutil.copy2(root / "_harness/.github/workflows/build-xess-1.9.1.yml", docs / "build-xess-1.9.1.yml")
for name in ("source.txt", "submodules.txt"):
    shutil.copy2(root / "evidence" / name, docs / name)
(docs / "INSTALL.txt").write_text(
    "Experimental Community Shaders 1.9.1 + NightHammer1000 PR #2704. AIO package.\n"
    "Install the inner MO2 ZIP as a separate mod. Its root is Skyrim Data.\n"
    "Disable the previous Community Shaders AIO/core and conflicting feature packages in the test profile.\n"
    "Keep the normal game/SKSE/Address Library requirements for your Skyrim runtime.\n"
    "All packaged feature settings and shaders must win conflicts together with the plugin.\n"
    "This includes the Upscaling feature; do not overwrite it with a different version.\n"
    "First allow shaders to compile, test XeSS SR with FG off, then test XeSS FG 2x.\n"
    "FG/XeLL require testing on ONEXPLAYER 3 / Arc B390. No performance or cache fix is claimed.\n"
    "Restricted upstream logo artwork omitted. Upstream code authorship and license notices preserved.\n",
    encoding="utf-8")
out = root / "dist-source"
out.mkdir(exist_ok=True)
with zipfile.ZipFile(out / "CommunityShaders-1.9.1-XeSS-corresponding-source.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for path in files:
        z.write(path, "source/" + path.relative_to(root).as_posix())
    for path in docs.rglob("*"):
        if path.is_file() and "licenses" not in path.relative_to(docs).parts:
            z.write(path, "build-recipe/" + path.relative_to(docs).as_posix())
    z.writestr("SOURCE-NOTE.txt", "Merged tracked sources and recursively pinned submodules. Restricted logo artwork excluded. Dependency versions and downloads are pinned by the included vcpkg manifest/baseline. See build-recipe for source commits and Windows build instructions.\n")
print("Source archive and notices prepared; restricted logo omitted.")
