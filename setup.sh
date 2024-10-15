apt-get update && apt-get install -y \
    python3.10 \
    python3-requests \
    git \
    wget


git clone https://github.com/seethroughlab/runpod-network-drive.git
cd runpod-network-drive
python3 get_models.py models.json /workspace