from data_manager import load_data, save_data

def create_product(branch_name, product_name):
    """Add a new product to the global product list."""
    data = load_data()
    branches = data['inventory']['branches']
    if product_name in data['products']:
        return False, f"Product {product_name} already exists."
    
    branches[branch_name][product_name] = []
    data['products'].append(product_name)
    save_data(data)
    
    return True, f"Product {product_name} created successfully."

def add_record(branch_name, product_name, quantity, record_date, emp_attendance):
    """Add a new production or sales record for a squad."""
    data = load_data()
    
    if product_name not in data['products']:
        return False, f"Product {product_name} does not exist. Create it first."
    
    if branch_name not in data['branches']:
        return False, f"Branch {branch_name} does not exist. Create it first."
    # Append the new record
    record = {"date": record_date, "emp_attendance": emp_attendance, "quantity": quantity}
    data['branches'][branch_name]['inventory'][product_name].append(record)
    save_data(data)
    
    return True, f"Record added for {branch_name}: {product_name} - {quantity} units on {record_date}."
