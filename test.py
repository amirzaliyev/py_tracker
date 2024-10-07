import json

# Example JSON structure
data = {
    "branches": {
        "1-seh": {
            "employees": ["ma", "ot", "ab"],
            "inventory": {
                "blok 20x40": [
                    {
                        "date": "01.10.2024",
                        "emp_attendance": ["ma", "ot", "ab"],
                        "quantity": 1240
                    },
                    {
                        "date": "02.10.2024",
                        "emp_attendance": ["ma", "ot", "ab"],
                        "quantity": 1240
                    }
                ],
                "Tumba": [],
                "Qizil tumba": []
            }
        }
    },
    "employees": {
        "ma": {
            "name": "Ma'mirjon",
            "emp_code": "ma",
            "branch": "1-seh",
            "salary": {}
        },
        "ot": {
            "name": "Otabek",
            "emp_code": "ot",
            "branch": "1-seh",
            "salary": {}
        },
        "ab": {
            "name": "Amelia Brown",
            "emp_code": "ab",
            "branch": "1-seh",
            "salary": {}
        }
    },
    "products": {
        "blok 20x40": {
            "price": 650,
            "description": "Concrete block size 20x40"
        },
        "Qizil blok 20x40": {
            "price": 650,
            "description": "Red concrete block size 20x40"
        },
        "Tumba": {
            "price": 1100,
            "description": "Furniture piece - Tumba"
        },
        "Qizil tumba": {
            "price": 1100,
            "description": "Red furniture piece - Tumba"
        },
        "blok 16x32": {
            "price": 450,
            "description": "Concrete block size 16x32"
        }
    }
}

def calculate_salaries(branch_name):
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

    # Update employee salary information in the data
    for emp_code, salary in salaries.items():
        if emp_code in data["employees"]:
            data["employees"][emp_code]["salary"]["total"] = salary

    return salaries

# Example usage
branch_name = "1-seh"
salaries = calculate_salaries(branch_name)
print(json.dumps(salaries, indent=4))  # Print calculated salaries
