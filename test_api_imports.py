#!/usr/bin/env python3
"""
Test what imports work in the API context
"""
import sys
import os

# Mimic the API import setup
sys.path.insert(0, 'src')

print("Testing API imports...")

modules_to_test = [
    'quantum_control.transmon_qubit',
    'quantum_control.two_qubit_gates', 
    'cryo_hardware.signal_chain',
    'quantum_ops.error_correction'
]

for module in modules_to_test:
    try:
        __import__(module)
        print(f"✅ {module}: IMPORT SUCCESS")
    except ImportError as e:
        print(f"❌ {module}: IMPORT FAILED - {e}")

print("\nTesting specific entanglement functions...")
try:
    from quantum_control.two_qubit_gates import EntanglementVerification
    print("✅ EntanglementVerification: IMPORT SUCCESS")
    
    # Test the function
    bell_state = EntanglementVerification.create_bell_state('CNOT')
    concurrence = EntanglementVerification.calculate_concurrence(bell_state)
    print(f"✅ Bell state creation: SUCCESS (concurrence={concurrence})")
    
except Exception as e:
    print(f"❌ Entanglement functions failed: {e}")
    import traceback
    traceback.print_exc()
