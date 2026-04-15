#!/bin/bash

echo "Starting moto-blackbox..."

# aktivuj venv (ak máš)
source ~/venvs/project-env/bin/activate

# spusti collector
echo "Starting collector..."
python software/collector/main.py &

# spusti processor
echo "Starting processor..."
python software/processor/main.py &

# počkaj na všetky procesy
wait
