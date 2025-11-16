#!/bin/bash
echo "🔬 Testing Quantum API Endpoints..."

# Wait for API to be ready
sleep 3

# Test root endpoint
echo "Testing root endpoint..."
curl -s http://localhost:8000/ && echo " ✅"

# Test entanglement
echo "Testing entanglement endpoint..."
curl -s 'http://localhost:8000/entanglement/bell_state?gate_type=CNOT' | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if data.get('success'):
        print('🎉 Entanglement working! Concurrence:', data['concurrence'])
    else:
        print('❌ Error:', data.get('message'))
except:
    print('❌ Failed to parse response')
"

echo "✅ Quantum API testing complete!"
