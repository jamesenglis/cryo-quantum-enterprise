from setuptools import setup, find_packages

setup(
    name="cryo-quantum-enterprise",
    version="0.1.0",
    description="Enterprise-grade cryogenic quantum computing control system",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0", 
        "matplotlib>=3.7.0",
        "pandas>=2.0.0",
        "qutip>=4.7.0",
        "jax>=0.4.0",
        "jaxlib>=0.4.0",
    ],
    python_requires=">=3.9",
)
