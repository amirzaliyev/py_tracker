from data_manager import load_data, save_data

def add_employee(branch_name, employee_name):
    """Add a new employee to a squad."""
    data = load_data()
    current_branch = data['branches'][branch_name]
    employees= data['employees']

    # Create an employee code 
    employee_code = employee_name[:2].lower()
    if employee_code in employees.keys():
        employee_code = employee_name[:3].lower()
        if employee_code in employees.keys():
            return False, f"Employee not added to {branch_name}"

    current_branch['employees'].append(employee_code)
    employees[employee_code] = {"name": employee_name, "emp_code": employee_code, "branch": branch_name, "salary": 0}
    save_data(data)
    
    return True, f"Employee {employee_name} added to {branch_name}."

def remove_employee(branch_name, emp_name):
    """Remove an employee from a squad."""
    data = load_data()
    employees = data['employees']
    emp_code = ""
    for e_code in employees.keys():
        if employees[e_code]['name'] == emp_name:
            emp_code = e_code
    
    if emp_code not in data['branches'][branch_name]['employees']:
        return False, f"Employee {emp_code} not found in {branch_name}."
    
    data['branches'][branch_name]['employees'].remove(emp_code)
    del data["employees"][emp_code]
    save_data(data)
    return True, f"Employee {emp_code} removed from {branch_name}."

def list_employees(branch_name):
    """List all employees in a squad."""
    data = load_data()
    employees = data['branches'].get(branch_name, {})
    
    if not employees:
        return f"No employees found in {branch_name}."
    
    return "\n".join([f"{code}: {name}" for code, name in employees.items()])


def calculate_salary(branch_name):
    """Calculate salaries in a specific branch"""
    # Load existing data
    data = load_data()

    # Get the branch data
    branch = data["branches"].get(branch_name)
    if not branch:
        return f"Branch '{branch_name}' does not exist."

    employees = branch["employees"]
    inventory = branch["inventory"]
    
    # Initialize salary dictionary
    salaries = {emp_code: 0 for emp_code in employees}

    # Loop through each product in the inventory
    for product, records in inventory.items():
        if not records:  # Skip if no records for the product
            continue

        # Get product price
        product_price = data["products"].get(product, {}).get("price", 0)

        # Loop through the records for this product
        for record in records:
            quantity = record["quantity"]
            emp_attendance = record["emp_attendance"]
            num_employees = len(emp_attendance)

            # Calculate salary for each employee present
            if num_employees > 0:
                salary_per_employee = (quantity * product_price) / num_employees
                for emp_code in emp_attendance:
                    if emp_code in salaries:
                        salaries[emp_code] += salary_per_employee

    # 
    message = []

    # Update employee salary information in the data
    for emp_code, salary in salaries.items():
        salary = round(salary, -3)
        if emp_code in data["employees"]:
            data["employees"][emp_code]["salary"] = salary
            message.append(f"{data['employees'][emp_code]['name']}: {salary}")
    
    save_data(data)
    return "\n\n   💰".join(message)