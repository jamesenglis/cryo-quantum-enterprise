#!/bin/bash
echo "🚀 Starting Cryo Quantum Enterprise System..."

# Kill any existing API processes
echo "Stopping any existing quantum API..."
pkill -f "python.*quantum_api" 2>/dev/null || true
sleep 2

# Start the quantum API
echo "Starting Quantum REST API..."
python src/api/quantum_api.py
