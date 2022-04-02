sudo apt-get install git build-essential cmake python3 python3-dev python3-pip python3-venv clang
git submodule update --init --recursive

python3 -m venv .venv
source .venv/bin/activate

cd SEAL-Python
python3 -m pip install -r requirements.txt mypy

# Build the SEAL lib
cd SEAL
cmake -S . -B build -DSEAL_USE_MSGSL=OFF -DSEAL_USE_ZLIB=OFF -DSEAL_USE_ZSTD=OFF -D CMAKE_CXX_COMPILER="clang" -D CMAKE_C_COMPILER="clang"

cmake --build build
cd ..

python3 setup.py build_ext -i
mv seal.cpython* ../
cd ..

stubgen -m seal -o stubs