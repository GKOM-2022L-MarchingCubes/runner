@echo off
mkdir build\assets
pushd visualizer
cargo build --release
copy target\release\visualizer.exe ..\build
xcopy /e /y assets ..\build\assets
popd
@echo on
