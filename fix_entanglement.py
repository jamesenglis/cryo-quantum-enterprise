"""
Quick fix for entanglement endpoint issues
"""
import sys
import os
sys.path.insert(0, 'src')

# Test the entanglement functions directly
try:
    from quantum_control.two_qubit_gates import EntanglementVerification
    import numpy as np
    
    print("Testing entanglement functions...")
    
    # Test CNOT Bell state
    bell_state_cnot = EntanglementVerification.create_bell_state('CNOT')
    concurrence_cnot = EntanglementVerification.calculate_concurrence(bell_state_cnot)
    print(f"✅ CNOT Bell state: concurrence = {concurrence_cnot}")
    print(f"   State: {bell_state_cnot}")
    
    # Test CZ Bell state  
    bell_state_cz = EntanglementVerification.create_bell_state('CZ')
    concurrence_cz = EntanglementVerification.calculate_concurrence(bell_state_cz)
    print(f"✅ CZ Bell state: concurrence = {concurrence_cz}")
    print(f"   State: {bell_state_cz}")
    
    # Test JSON serialization
    state_list = [float(x.real) for x in bell_state_cnot]
    print(f"✅ JSON serializable: {state_list}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
