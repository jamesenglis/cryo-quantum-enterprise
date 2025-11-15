"""
Industry-standard cryogenic signal chain simulation.
Models actual hardware used in quantum computing labs.
"""
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Tuple
import numpy as np
from scipy import signal
import logging

class TemperatureStage(Enum):
    """Standard dilution refrigerator stages"""
    ROOM_TEMP = 300.0    # Kelvin
    STILL = 0.8          # Kelvin  
    COLD = 0.1           # Kelvin
    MIXING_CHAMBER = 0.015  # Kelvin (typical qubit temperature)

@dataclass
class AmplifierSpec:
    """Specifications for cryogenic amplifiers"""
    gain: float  # dB
    noise_temperature: float  # Kelvin
    bandwidth: Tuple[float, float]  # Hz
    compression: float  # dBm
    stage: TemperatureStage

class CryogenicAmplifier:
    """
    HEMT amplifier model used at 4K stage in quantum computers.
    Industry standard from companies like Low Noise Factory.
    """
    
    def __init__(self, spec: AmplifierSpec):
        self.spec = spec
        self.logger = logging.getLogger(__name__)
        
    def process_signal(self, input_signal: np.ndarray, 
                      center_frequency: float = 6e9) -> np.ndarray:
        """
        Process signal through cryogenic amplifier with realistic noise.
        
        Args:
            input_signal: Input signal (complex baseband)
            center_frequency: Center frequency in Hz
            
        Returns:
            Amplified signal with cryogenic noise
        """
        # Convert to power for gain calculation
        input_power = np.mean(np.abs(input_signal) ** 2)
        
        # Apply gain (convert dB to linear)
        gain_linear = 10 ** (self.spec.gain / 20)
        amplified = input_signal * gain_linear
        
        # Add cryogenic noise (Johnson-Nyquist)
        k_B = 1.380649e-23  # Boltzmann constant
        bandwidth = self.spec.bandwidth[1] - self.spec.bandwidth[0]
        noise_power = k_B * self.spec.noise_temperature * bandwidth
        noise_std = np.sqrt(noise_power)
        
        # Complex Gaussian noise
        complex_noise = (np.random.normal(0, noise_std, len(input_signal)) + 
                        1j * np.random.normal(0, noise_std, len(input_signal)))
        
        output_signal = amplified + complex_noise
        
        self.logger.debug(
            f"Cryo amp: gain={self.spec.gain}dB, "
            f"noise_temp={self.spec.noise_temperature}K, "
            f"input_power={10*np.log10(input_power*1000):.1f}dBm"
        )
        
        return output_signal

class CryogenicControlSystem:
    """
    Complete cryogenic control system following industry patterns.
    Similar to systems from Zurich Instruments, Quantum Machines.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Standard cryogenic amplifier chain
        self.amplifiers = {
            '4K': CryogenicAmplifier(
                AmplifierSpec(
                    gain=35.0,
                    noise_temperature=2.0,
                    bandwidth=(4e9, 8e9),
                    compression=10.0,
                    stage=TemperatureStage.STILL
                )
            ),
            'MXC': CryogenicAmplifier(
                AmplifierSpec(
                    gain=25.0,
                    noise_temperature=5.0,
                    bandwidth=(4e9, 8e9),
                    compression=5.0,
                    stage=TemperatureStage.MIXING_CHAMBER
                )
            )
        }
        
        self.qubits = []
        self.calibration_data = {}
        
    def add_qubit(self, qubit_spec):
        """Add qubit to control system"""
        # Import here to avoid circular imports
        from quantum_control.transmon_qubit import TransmonQubit
        qubit = TransmonQubit(qubit_spec)
        self.qubits.append(qubit)
        self.logger.info(f"Added qubit with frequency {qubit_spec.frequency} GHz")
        return qubit
        
    def run_readout(self, qubit_index: int, shots: int = 1000) -> Dict:
        """
        Run full cryogenic readout chain.
        
        Args:
            qubit_index: Index of qubit to measure
            shots: Number of measurement shots
            
        Returns:
            Readout results with signal chain information
        """
        if qubit_index >= len(self.qubits):
            raise ValueError(f"Qubit index {qubit_index} out of range")
            
        qubit = self.qubits[qubit_index]
        
        # Generate ideal readout signal
        ideal_signal = self._generate_readout_signal(qubit)
        
        # Process through cryogenic signal chain
        signal_4k = self.amplifiers['4K'].process_signal(ideal_signal)
        signal_mxc = self.amplifiers['MXC'].process_signal(signal_4k)
        
        # Simulate measurement
        results = qubit.simulate_measurement(shots)
        
        # Add signal chain information
        results.update({
            'signal_power_4k': np.mean(np.abs(signal_4k) ** 2),
            'signal_power_mxc': np.mean(np.abs(signal_mxc) ** 2),
            'snr_improvement': self._calculate_snr_improvement(ideal_signal, signal_mxc)
        })
        
        return results
    
    def _generate_readout_signal(self, qubit, duration: float = 100.0) -> np.ndarray:
        """Generate readout signal for qubit measurement"""
        t = np.linspace(0, duration, int(duration * 10))  # 10 GS/s
        frequency = qubit.spec.readout_frequency * 1e9  # Convert to Hz
        amplitude = qubit.spec.readout_amplitude
        
        # Simple tone for readout
        readout_signal = amplitude * np.exp(2j * np.pi * frequency * t * 1e-9)  # ns to s
        
        return readout_signal
    
    def _calculate_snr_improvement(self, input_signal: np.ndarray, 
                                 output_signal: np.ndarray) -> float:
        """Calculate SNR improvement through signal chain"""
        input_snr = np.mean(np.abs(input_signal) ** 2) / np.var(input_signal)
        output_snr = np.mean(np.abs(output_signal) ** 2) / np.var(output_signal)
        return output_snr / input_snr

# Example usage
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Create control system
    control_system = CryogenicControlSystem()
    
    # Add a qubit
    from quantum_control.transmon_qubit import QubitSpec
    qubit_spec = QubitSpec(
        frequency=5.0,
        anharmonicity=-0.3,
        t1=10000,
        t2=5000,
        readout_frequency=6.5,
        readout_amplitude=0.01
    )
    
    qubit = control_system.add_qubit(qubit_spec)
    
    # Run readout
    results = control_system.run_readout(0, shots=1000)
    print("Readout results:", results)
