"""
Tests for quantum error correction system
"""
import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from quantum_ops.error_correction import (
    QuantumErrorCorrection, QECCode, 
    SurfaceCode, RepetitionCode
)

class TestQuantumErrorCorrection:
    """Test quantum error correction functionality"""
    
    def test_surface_code_initialization(self):
        """Test surface code initialization"""
        surface_code = SurfaceCode(distance=3)
        assert surface_code.distance == 3
        assert len(surface_code.measurement_results) == 0
    
    def test_repetition_code_initialization(self):
        """Test repetition code initialization"""
        rep_code = RepetitionCode(repetitions=3)
        assert rep_code.repetitions == 3
    
    def test_surface_code_encoding(self):
        """Test surface code logical qubit encoding"""
        surface_code = SurfaceCode(distance=3)
        test_state = np.array([1, 0])  # |0⟩ state
        
        encoded_state = surface_code.encode_logical_qubit(test_state)
        assert encoded_state.shape[0] == 2 * (2**3)  # Check encoding size
    
    def test_repetition_code_encoding(self):
        """Test repetition code logical qubit encoding"""
        rep_code = RepetitionCode(repetitions=3)
        test_state = np.array([1, 0])  # |0⟩ state
        
        encoded_state = rep_code.encode_logical_qubit(test_state)
        assert encoded_state.shape[0] == 2**3  # Check encoding size
    
    def test_qec_surface_code_cycle(self):
        """Test full QEC cycle with surface code"""
        qec = QuantumErrorCorrection(QECCode.SURFACE_CODE)
        test_state = np.array([1, 0])
        
        corrected_state, results = qec.run_qec_cycle(test_state)
        
        assert 'code_type' in results
        assert 'errors_detected' in results
        assert 'logical_error_rate' in results
        assert results['code_type'] == 'surface_code'
    
    def test_qec_repetition_code_cycle(self):
        """Test full QEC cycle with repetition code"""
        qec = QuantumErrorCorrection(QECCode.REPETITION_CODE)
        test_state = np.array([1, 0])
        
        corrected_state, results = qec.run_qec_cycle(test_state)
        
        assert 'code_type' in results
        assert 'errors_detected' in results
        assert 'logical_error_rate' in results
        assert results['code_type'] == 'repetition_code'

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
