"""
Direct fix for the entanglement endpoint
"""
import re

# Read the API file
with open('src/api/quantum_api.py', 'r') as f:
    lines = f.readlines()

# Find the create_bell_state function and replace it
new_function = '''@app.get("/entanglement/bell_state")
async def create_bell_state(gate_type: str = 'CNOT'):
    """Create and verify Bell state entanglement - FIXED VERSION"""
    try:
        print(f"Creating Bell state with gate_type: {gate_type}")
        
        if not QUANTUM_IMPORTS_WORKING:
            print("Using demo mode (quantum imports not working)")
            return {
                "bell_state_type": gate_type,
                "concurrence": 0.99,
                "entanglement_strength": "maximal",
                "state_vector": [0.707, 0.0, 0.0, 0.707],
                "mode": "demo",
                "message": "Demo Bell state created successfully"
            }
        
        # Validate gate type
        if gate_type not in ['CNOT', 'CZ']:
            return {
                "error": "Invalid gate_type",
                "message": "gate_type must be 'CNOT' or 'CZ'",
                "valid_options": ["CNOT", "CZ"]
            }
        
        print("Creating actual Bell state...")
        bell_state = EntanglementVerification.create_bell_state(gate_type)
        print(f"Bell state created: {bell_state}")
        
        concurrence = EntanglementVerification.calculate_concurrence(bell_state)
        print(f"Concurrence calculated: {concurrence}")
        
        # Convert to JSON-serializable format
        state_list = []
        for i, val in enumerate(bell_state):
            if hasattr(val, 'real'):
                state_list.append(float(val.real))
            else:
                state_list.append(float(val))
        
        print("Returning successful response")
        return {
            "bell_state_type": gate_type,
            "concurrence": float(concurrence),
            "entanglement_strength": "maximal" if concurrence > 0.9 else "partial",
            "state_vector": state_list,
            "message": f"Bell state created successfully with {gate_type} gate",
            "success": True
        }
        
    except Exception as e:
        error_msg = f"Entanglement creation failed: {str(e)}"
        print(f"ERROR: {error_msg}")
        import traceback
        traceback.print_exc()
        return {
            "error": "Internal server error",
            "message": error_msg,
            "success": False
        }'''

# Find and replace the function
in_function = False
function_start = -1
function_end = -1
new_lines = []

for i, line in enumerate(lines):
    if '@app.get("/entanglement/bell_state")' in line:
        function_start = i
        in_function = True
        # Add the new function
        new_lines.append(new_function + '\n')
    elif in_function and line.strip() and not line.startswith(' ') and not line.startswith('@') and i > function_start:
        # Found the next function, end of current function
        in_function = False
    elif not in_function:
        new_lines.append(line)

# If we found and replaced the function, write the file
if function_start != -1:
    with open('src/api/quantum_api.py', 'w') as f:
        f.writelines(new_lines)
    print("✅ Successfully replaced entanglement endpoint")
else:
    print("❌ Could not find entanglement endpoint to replace")
    print("The API file structure might be different than expected")
