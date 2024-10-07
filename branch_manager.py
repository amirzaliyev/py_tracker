from data_manager import load_data, save_data

def create_branch(branch_name):
    """Create a new branch."""
    data = load_data()
    
    if branch_name in data['branches']:
        return False, f"Branch {branch_name} already exists."
    
    # Add the new branch
    data['branches'][branch_name] = {"employees": [], "inventory":{}}
    save_data(data)
    
    return True, f"Branch {branch_name} created successfully."

def delete_branch(branch_name):
    """Delete an existing branch."""
    data = load_data()
    
    if branch_name not in data['branches']:
        return False, f"Branch {branch_name} does not exist."
    
    # Remove the branch and its employees
    del data['branches'][branch_name]
    save_data(data)
    
    return True, f"Branch {branch_name} deleted successfully."

def list_branches():
    """List all available branchs."""
    data = load_data()
    branches = [branch for branch in data['branches'].keys()]
    if not branches:
        return "No branchs found."
    
    return "\n\n   💰".join(branches)
