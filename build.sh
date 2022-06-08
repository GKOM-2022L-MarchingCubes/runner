cd visualizer
cargo build
mkdir -p ../build
cp target/debug/visualizer.exe ../build/.
cp -r assets ../build/.
