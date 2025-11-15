#!/usr/bin/env python3
"""
Simple test to verify all imports work
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from quantum_control.transmon_qubit import TransmonQubit, QubitSpec
    print("✅ quantum_control imports successful")
    
    from cryo_hardware.signal_chain import CryogenicControlSystem
    print("✅ cryo_hardware imports successful")
    
    # Test creating objects
    spec = QubitSpec(
        frequency=5.0,
        anharmonicity=-0.3, 
        t1=10000,
        t2=5000,
        readout_frequency=6.5,
        readout_amplitude=0.01
    )
    qubit = TransmonQubit(spec)
    print("✅ Qubit creation successful")
    
    control_system = CryogenicControlSystem()
    print("✅ Control system creation successful")
    
    print("\n🎉 All imports and object creation working!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Current Python path: {sys.path}")
