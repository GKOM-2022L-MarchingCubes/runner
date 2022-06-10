mkdir -p build
cd visualizer
cargo build --release
cp target/debug/visualizer.exe ../build/.
cp -r assets ../build/.
