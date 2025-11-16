"""
Update the entanglement endpoint in the API file
"""
import re

# Read the current API file
with open('src/api/quantum_api.py', 'r') as f:
    content = f.read()

# Find and replace the entanglement endpoint
old_entanglement = '''@app.get("/entanglement/bell_state")
async def create_bell_state(gate_type: str = 'CNOT'):
    """Create and verify Bell state entanglement"""
    if not QUANTUM_IMPORTS_WORKING:
        # Return demo Bell state data
        return {
            "bell_state_type": gate_type,
            "concurrence": 0.99,
            "entanglement_strength": "maximal",
            "state_vector": [0.707, 0.0, 0.0, 0.707],
            "mode": "demo"
        }
    
    try:
        bell_state = EntanglementVerification.create_bell_state(gate_type)
        concurrence = EntanglementVerification.calculate_concurrence(bell_state)
        
        # Convert to Python native types for JSON serialization
        state_list = [float(x.real) for x in bell_state]  # Just take real parts
        
        return {
            "bell_state_type": gate_type,
            "concurrence": float(concurrence),
            "entanglement_strength": "maximal" if concurrence > 0.9 else "partial",
            "state_vector": state_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entanglement creation failed: {str(e)}")'''

new_entanglement = '''@app.get("/entanglement/bell_state")
async def create_bell_state(gate_type: str = 'CNOT'):
    """Create and verify Bell state entanglement - ROBUST VERSION"""
    try:
        if not QUANTUM_IMPORTS_WORKING:
            # Return demo Bell state data
            return {
                "bell_state_type": gate_type,
                "concurrence": 0.99,
                "entanglement_strength": "maximal",
                "state_vector": [0.707, 0.0, 0.0, 0.707],
                "mode": "demo"
            }
        
        # Validate gate type
        if gate_type not in ['CNOT', 'CZ']:
            raise HTTPException(status_code=400, detail="gate_type must be 'CNOT' or 'CZ'")
        
        bell_state = EntanglementVerification.create_bell_state(gate_type)
        concurrence = EntanglementVerification.calculate_concurrence(bell_state)
        
        # Convert to Python native types for JSON serialization
        state_list = []
        for x in bell_state:
            if isinstance(x, (int, float)):
                state_list.append(float(x))
            elif hasattr(x, 'real'):
                state_list.append(float(x.real))
            else:
                state_list.append(float(x))
        
        return {
            "bell_state_type": gate_type,
            "concurrence": float(concurrence),
            "entanglement_strength": "maximal" if concurrence > 0.9 else "partial",
            "state_vector": state_list,
            "message": f"Bell state created successfully with {gate_type} gate"
        }
    except HTTPException:
        raise
    except Exception as e:
        # Provide more detailed error information
        error_detail = f"Entanglement creation failed: {str(e)}"
        print(f"Entanglement error: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)'''

# Replace the content
if old_entanglement in content:
    content = content.replace(old_entanglement, new_entanglement)
    print("✅ Updated entanglement endpoint")
else:
    print("❌ Could not find the entanglement endpoint to update")

# Write the updated content
with open('src/api/quantum_api.py', 'w') as f:
    f.write(content)

print("✅ API file updated")
