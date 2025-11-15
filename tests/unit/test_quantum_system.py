"""
Unit tests for quantum control system.
Industry-standard testing practices.
"""
import pytest
import numpy as np
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from quantum_control.transmon_qubit import TransmonQubit, QubitSpec
from cryo_hardware.signal_chain import CryogenicControlSystem, AmplifierSpec, TemperatureStage

class TestTransmonQubit:
    """Test transmon qubit functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.qubit_spec = QubitSpec(
            frequency=5.0,
            anharmonicity=-0.3,
            t1=10000,
            t2=5000,
            readout_frequency=6.5,
            readout_amplitude=0.01
        )
        self.qubit = TransmonQubit(self.qubit_spec)
    
    def test_initial_state(self):
        """Test qubit initializes in |0⟩ state"""
        probs = self.qubit.get_state_probabilities()
        assert probs['|0⟩'] == 1.0
        assert probs['|1⟩'] == 0.0
    
    def test_x_gate(self):
        """Test X gate functionality"""
        self.qubit.apply_x_gate()
        probs = self.qubit.get_state_probabilities()
        assert probs['|1⟩'] == 1.0
    
    def test_drag_pulse_generation(self):
        """Test DRAG pulse generation"""
        I, Q = self.qubit.generate_drag_pulse(duration=20.0, amplitude=0.1)
        assert len(I) == len(Q)
        assert I.shape == Q.shape
        assert np.max(I) > 0  # Should have non-zero amplitude
    
    def test_measurement_statistics(self):
        """Test measurement produces valid statistics"""
        results = self.qubit.simulate_measurement(shots=1000)
        assert '0' in results
        assert '1' in results
        assert results['0'] + results['1'] == 1000

class TestCryogenicSystem:
    """Test cryogenic control system"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.control_system = CryogenicControlSystem()
        
        # Add a test qubit
        qubit_spec = QubitSpec(
            frequency=5.0,
            anharmonicity=-0.3,
            t1=10000,
            t2=5000,
            readout_frequency=6.5,
            readout_amplitude=0.01
        )
        self.qubit = self.control_system.add_qubit(qubit_spec)
    
    def test_qubit_addition(self):
        """Test adding qubits to control system"""
        assert len(self.control_system.qubits) == 1
        assert self.control_system.qubits[0] == self.qubit
    
    def test_readout_chain(self):
        """Test complete readout chain"""
        results = self.control_system.run_readout(0, shots=100)
        assert '0' in results
        assert '1' in results
        assert 'snr_improvement' in results
        assert results['snr_improvement'] > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
