sudo apt-get install git build-essential cmake python3.10 python3.10-dev python3-pip python3.10-venv clang
git submodule update --init --recursive

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r dev-requirements.txt

cd SEAL-Python
python3 -m pip install -r requirements.txt

# Build the SEAL lib
cd SEAL
cmake -S . -B build -DSEAL_USE_MSGSL=OFF -DSEAL_USE_ZLIB=OFF -DSEAL_USE_ZSTD=OFF -D CMAKE_CXX_COMPILER="clang" -D CMAKE_C_COMPILER="clang"

cmake --build build -j9
cd ..

python3.10 setup.py build_ext -i
# mv seal.cpython* ../
# cd ..

# This will overwrite?
# stubgen -m seal -o stubs
