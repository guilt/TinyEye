#!/bin/bash
# Download TAESD weights (tiny ~4.7MB each)
set -e
curl -L -o taesd_encoder.pth https://github.com/madebyollin/taesd/raw/main/taesd_encoder.pth
curl -L -o taesd_decoder.pth https://github.com/madebyollin/taesd/raw/main/taesd_decoder.pth
echo "Weights downloaded. Ready to run: python tinyeye_encode.py yourimage.jpg"
