"""Compile the real frame-start methods against a minimal mocked XeLL runtime."""
import pathlib, subprocess, tempfile
src = pathlib.Path("src/Features/Upscaling/IntelXeSSFrameGeneration.cpp").read_text(encoding="utf-8")
def method(signature):
    start = src.index(signature)
    opening = src.index("{", start)
    depth = 1
    end = opening + 1
    while depth:
        depth += (src[end] == "{") - (src[end] == "}")
        end += 1
    return src[start:end]
methods = "\n".join(method(s) for s in (
    "bool IntelXeSSFrameGeneration::BeginFrame()",
    "bool IntelXeSSFrameGeneration::BeginFrame(uint64_t globalsFrame)",
    "bool IntelXeSSFrameGeneration::StartFrameUnlocked("))
harness = r'''
#include <cassert>
#include <cstdint>
#include <limits>
#include <mutex>
using xell_context_handle_t = void*;
using xell_result_t = int;
constexpr int XELL_SIMULATION_START = 0, XELL_INPUT_SAMPLE = 1;
struct IntelXeSSFrameGeneration {
    enum class FrameStage { Idle, Simulation, RenderSubmit, Present };
    std::mutex mutex_;
    bool initialized_ = true, taggedThisFrame_ = false, inputSampleSent_ = false;
    FrameStage frameStage_ = FrameStage::Idle;
    uint64_t lastGlobalsFrame_ = std::numeric_limits<uint64_t>::max();
    uint32_t currentPresentId_ = 0, nextPresentId_ = 1;
    xell_context_handle_t xellContext_ = this;
    struct Runtime { int sleep(void*, uint32_t) { return 0; } } xell_;
    bool CheckXeLLResult(int r, const char*) { return r == 0; }
    bool AddMarkerUnlocked(int) { return true; }
    bool BeginFrame();
    bool BeginFrame(uint64_t);
    bool StartFrameUnlocked(std::unique_lock<std::mutex>&, uint64_t);
};
'''
main = r'''
int main() {
    using FG = IntelXeSSFrameGeneration;
    FG fg;
    assert(fg.BeginFrame());
    const auto id = fg.currentPresentId_;
    assert(id == 1 && fg.frameStage_ == FG::FrameStage::Simulation);
    assert(fg.BeginFrame()); // repeated render hook must not allocate another ID
    assert(fg.currentPresentId_ == id);
    fg.frameStage_ = FG::FrameStage::RenderSubmit;
    fg.taggedThisFrame_ = true;
    assert(fg.BeginFrame());
    assert(fg.currentPresentId_ == id && fg.taggedThisFrame_);
    fg.frameStage_ = FG::FrameStage::Present;
    // Reproduce the old schedule: a new frame arrives while Present is blocked.
    // It must not synthesize PRESENT_END or change the tagged present ID.
    assert(!fg.BeginFrame(999));
    assert(fg.frameStage_ == FG::FrameStage::Present);
    assert(fg.currentPresentId_ == id && fg.taggedThisFrame_);
    assert(fg.BeginFrame());
    assert(fg.frameStage_ == FG::FrameStage::Present && fg.currentPresentId_ == id);
    // Matching AfterPresent returns the slot to Idle. Another present must get
    // a fresh ID even if the game's global/input counter hasn't advanced.
    fg.frameStage_ = FG::FrameStage::Idle;
    fg.taggedThisFrame_ = false;
    assert(fg.BeginFrame());
    assert(fg.currentPresentId_ == id + 1);
    assert(fg.frameStage_ == FG::FrameStage::Simulation);
    FG stopped;
    stopped.initialized_ = false;
    assert(!stopped.BeginFrame());
    assert(stopped.currentPresentId_ == 0);
}
'''
with tempfile.TemporaryDirectory() as tmp:
    p = pathlib.Path(tmp)
    source = p / "frame-test.cpp"
    source.write_text(harness + methods + main, encoding="utf-8")
    exe = p / "frame-test.exe"
    subprocess.run(["cl", "/nologo", "/std:c++20", "/EHsc", str(source), "/Fe:" + str(exe), "/Fo:" + str(p / "frame-test.obj")], check=True)
    subprocess.run([str(exe)], check=True)
print("PASS: real frame-start methods preserve in-flight ID/tags and allocate per-present IDs")
