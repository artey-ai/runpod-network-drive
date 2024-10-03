apt-get update && apt-get install -y \
    python3.10 \
    python3-requests \
    git \
    wget

python get_models.py models.json ./