# Install the Llama python library

## Why is this a separate script?
# Poetry does not support custom CMAKE args, and cannot change to GPU or CPU by itself.
# This script is a workaround for that.
# Run this outside of the folder

python -m venv .venv
source .env

source .venv/bin/activate

# Install the inference server

if [ "$TYPE" == "llama" ]; then
    if [ "$1" == "gpu" ]; then
        echo "GPU Installation"
        export LLAMA_CUBLAS=1
        CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python
        pip install -r gpu_requirements.txt
    else
        pip install llama-cpp-python
        pip install -r cpu_requirements.txt
    fi
else
    pip install -r cpu_requirements.txt
fi

# Install the Llama model from NFS
if [ "$1" == "models" ] || [ "$2" == "models" ]; then
    if [ -d "models" ]; then
        echo "Models folder already exists"
    else
        mkdir models
    fi

    sudo mount -o user -v -t nfs "$NFS_IP:/home/nfs/models" "$PWD/models"
    cp -r "models/$MODEL" .

    sudo umount -l "$PWD/models"
    mv "$MODEL" "models/$MODEL"
fi
