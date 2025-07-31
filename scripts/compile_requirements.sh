#!/bin/bash
echo "📦 Generiere requirements.txt aus requirements.in ..."
pip install --upgrade pip pip-tools
pip-compile requirements.in > requirements.txt
