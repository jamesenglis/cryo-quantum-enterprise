#!/usr/bin/env python3
"""
Enterprise Quantum Computing Demo
Shows full cryogenic quantum control stack in action.
"""
import sys
import os
import logging

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.quantum_control.transmon_qubit import TransmonQubit, QubitSpec
from src.cryo_hardware.signal_chain import CryogenicControlSystem

def main():
    """Run enterprise quantum computing demo"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    print("🚀 Enterprise Cryogenic Quantum Computing Demo")
    print("=" * 50)
    
    # Create cryogenic control system
    logger.info("Initializing cryogenic control system...")
    control_system = CryogenicControlSystem()
    
    # Create qubits with realistic specs (like IBM Quantum processors)
    qubit_specs = [
        QubitSpec(
            frequency=5.0 + i * 0.1,  # Different frequencies for each qubit
            anharmonicity=-0.3,
            t1=10000,
            t2=5000,
            readout_frequency=6.5 + i * 0.05,
            readout_amplitude=0.01
        )
        for i in range(3)  # Create 3 qubits
    ]
    
    # Add qubits to control system
    for i, spec in enumerate(qubit_specs):
        qubit = control_system.add_qubit(spec)
        print(f"✅ Qubit {i}: {spec.frequency:.2f} GHz")
    
    print("\n🧪 Running Quantum Experiments:")
    print("-" * 30)
    
    # Experiment 1: Single qubit operations
    print("\n1. Single Qubit Operations:")
    qubit = control_system.qubits[0]
    print(f"   Initial state: {qubit.get_state_probabilities()}")
    
    # Apply X gate
    qubit.apply_x_gate()
    print(f"   After X gate: {qubit.get_state_probabilities()}")
    
    # Measure
    results = control_system.run_readout(0, shots=1000)
    print(f"   Measurement: |0⟩: {results['0']}, |1⟩: {results['1']}")
    
    # Experiment 2: Multiple qubit readout
    print("\n2. Multi-Qubit Readout:")
    for i in range(len(control_system.qubits)):
        results = control_system.run_readout(i, shots=500)
        print(f"   Qubit {i}: |0⟩: {results['0']:3d}, |1⟩: {results['1']:3d}, "
              f"SNR improvement: {results['snr_improvement']:.2f}x")
    
    # Experiment 3: Cryogenic performance
    print("\n3. Cryogenic System Performance:")
    print(f"   Number of amplifiers: {len(control_system.amplifiers)}")
    print(f"   Qubit temperature: {control_system.qubits[0].temperature * 1000:.1f} mK")
    print(f"   Typical T1: {control_system.qubits[0].spec.t1 / 1000:.1f} μs")
    print(f"   Typical T2: {control_system.qubits[0].spec.t2 / 1000:.1f} μs")
    
    print("\n🎉 Demo completed successfully!")
    print("   This simulates real quantum hardware control used by:")
    print("   - IBM Quantum • Google Quantum AI • Rigetti Computing")

if __name__ == "__main__":
    main()
