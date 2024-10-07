from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
from branch_manager import create_branch, delete_branch, list_branches
from employee_manager import add_employee, remove_employee, list_employees, calculate_salary
from inventory_manager import create_product, add_record
from data_manager import load_data
import datetime

# Define the constants for conversation stages
BRANCH_NAME, EMPLOYEE_NAME, EMP_ATTENDANCE, PRODUCT_NAME, RECORD_DATE, RECORD_QUANTITY = range(6)

# Start Command
async def start(update: Update, context: CallbackContext):
    """Send a welcome message and show the admin options."""
    keyboard = [['/create_branch', '/delete_branch'],
                ['/list_branches', '/add_employee'],
                ['/remove_employee', '/list_employees'],
                ['/create_product', '/add_record', '/list_records']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
    await update.message.reply_text('Welcome! Choose an option:', reply_markup=reply_markup)


# Handle create branch
async def create_branch_handler(update: Update, context: CallbackContext):
    await update.message.reply_text("Enter the new branch name:")
    return BRANCH_NAME

async def branch_name_received(update: Update, context: CallbackContext):
    branch_name = update.message.text.strip()
    success, message = create_branch(branch_name)
    await update.message.reply_text(message)
    return ConversationHandler.END

# Delete Squad Command
async def delete_branch_handler(update: Update, context: CallbackContext):
    """Show all branchs and ask which one to delete."""
    data = load_data()
    branchs = [branch for branch in data['branches'].keys()]
    
    if not branchs:
        await update.message.reply_text("No branchs available.")
        return ConversationHandler.END
    
    keyboard = [[branch] for branch in branchs]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text('Select a branch to delete:', reply_markup=reply_markup)
    return BRANCH_NAME

async def delete_branch_received(update: Update, context: CallbackContext):
    """Delete the selected branch."""
    branch_name = update.message.text.strip()
    success, message = delete_branch(branch_name)
    
    await update.message.reply_text(message)
    return ConversationHandler.END


# List Squads Command
async def list_branches_handler(update: Update, context: CallbackContext):
    """List all squads."""
    branches = list_branches()
    await update.message.reply_text(f"Existing Squads:\n\n   💰{branches}")

# Add Employee Command
async def add_employee_handler(update: Update, context: CallbackContext):
    """Ask for the squad to add an employee."""
    data = load_data()
    branches = [branch for branch in data['branches'].keys()]
    
    if not branches:
        await update.message.reply_text("No branches found. Create a branch first.")
        return ConversationHandler.END
    
    keyboard = [[branch] for branch in branches]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Select a branch to add an employee:", reply_markup=reply_markup)
    return BRANCH_NAME

async def add_employee_branch_received(update: Update, context: CallbackContext):
    """Ask for the employee name to add to the squad."""
    context.user_data['branch_name'] = update.message.text.strip()
    await update.message.reply_text("Enter the employee's name:", reply_markup=ReplyKeyboardRemove())
    return EMPLOYEE_NAME

async def add_employee_name_received(update: Update, context: CallbackContext):
    """Ask for the employee code."""
    branch_name = context.user_data['branch_name']
    employee_name = update.message.text.strip()
    success, message = add_employee(branch_name, employee_name)  

    await update.message.reply_text(message)  
    return ConversationHandler.END


# Remove Employee Command
async def remove_employee_handler(update: Update, context: CallbackContext):
    """Ask for the squad from which to remove an employee."""
    data = load_data()
    branches = [branch for branch in data['branches'].keys()]
    
    if not branches:
        await update.message.reply_text("No branches found.")
        return ConversationHandler.END
    
    keyboard = [[branch] for branch in branches]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Select a branch to remove an employee:", reply_markup=reply_markup)
    return BRANCH_NAME

async def remove_employee_branch_received(update: Update, context: CallbackContext):
    """Ask for the employee code to remove."""
    context.user_data['branch_name'] = update.message.text.strip()
    branch_name = context.user_data['branch_name']
    data = load_data()
    
    if not data['branches'][branch_name]:
        await update.message.reply_text(f"No employees found in {branch_name}.")
        return ConversationHandler.END
    
    emp_codes = data['branches'][branch_name]['employees']
    emp_names = []
    for emp_code in emp_codes:
        emp_names.append(data['employees'][emp_code]['name'])

    
    keyboard = [[emp] for emp in emp_names]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Select an employee to remove:", reply_markup=reply_markup)
    return EMPLOYEE_NAME

async def remove_employee_name_received(update: Update, context: CallbackContext):
    """Remove the employee from the selected squad."""
    branch_name = context.user_data['branch_name']
    employee_name = update.message.text.strip().lower()

    success, message = remove_employee(branch_name, employee_name)
    
    await update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def calculate_salary_handler(update: Update, context: CallbackContext):
    """Ask for the branch to calculate salaries"""
    data = load_data()
    branches = [branch for branch in data['branches'].keys()]

    if not branches:
        await update.message.reply_text("No branches found.")
        return ConversationHandler.END
    
    keyboard = [[branch] for branch in branches]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Select a branch to calculate salaries:", reply_markup=reply_markup)
    return BRANCH_NAME

async def calculate_salary_branch_received(update:Update, context: CallbackContext):
    """Calculate employee salaries from selected branch"""
    branch_name = update.message.text.strip()

    message = calculate_salary(branch_name)

    await update.message.reply_text(f"Salaries💰💰:\n\n   💰{message}", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# # List Employees in Squad Command
# async def list_employees(update: Update, context: CallbackContext):
#     """List all employees in a specific squad."""
#     data = load_data()
#     squads = [squad for squad in data['employees']]
    
#     if not squads:
#         await update.message.reply_text("No squads found.")
#         return
    
#     keyboard = [[squad] for squad in squads]
#     reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
#     await update.message.reply_text("Select a squad to list employees:", reply_markup=reply_markup)
#     return SQUAD_NAME

# async def list_employees_squad_received(update: Update, context: CallbackContext):
#     """List employees in the selected squad."""
#     squad_name = update.message.text.strip()
#     data = load_data()
    
#     employees = data['employees'][squad_name]
    
#     if not employees:
#         await update.message.reply_text(f"No employees found in {squad_name}.")
#         return ConversationHandler.END
    
#     employee_list = "\n".join([f"{code}: {name}" for code, name in employees.items()])
#     await update.message.reply_text(f"Employees in {squad_name}:\n{employee_list}")
#     return ConversationHandler.END

# Create Product Command
async def create_product_handler(update: Update, context: CallbackContext):
    """Ask for the squad to create a product for."""
    data = load_data()
    branches = [branch for branch in data['inventory']['branches']]
    
    if not branches:
        await update.message.reply_text("No branches found. Create a branch first.")
        return ConversationHandler.END
    
    keyboard = [[branch] for branch in branches]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Select a branch to create a product:", reply_markup=reply_markup)
    return BRANCH_NAME

async def create_product_branch_received(update: Update, context: CallbackContext):
    """Ask for the product name to add to the branch's inventory."""
    context.user_data['branch_name'] = update.message.text.strip()
    await update.message.reply_text("Enter the product name:", reply_markup=ReplyKeyboardRemove())
    return PRODUCT_NAME

async def create_product_name_received(update: Update, context: CallbackContext):
    """Add the product to the branch's inventory."""
    branch_name = context.user_data['branch_name']
    product_name = update.message.text.strip()

    success, message = create_product(branch_name, product_name)
    
    await update.message.reply_text(message)
    return ConversationHandler.END


# Add Record Command
async def add_record_handler(update: Update, context: CallbackContext):
    """Ask for the branch to add a record for."""
    data = load_data()
    branches = [branch for branch in data['branches'].keys()]
    
    if not branches:
        await update.message.reply_text("No branches found.")
        return ConversationHandler.END
    
    # Add a "Back" button
    keyboard = [[branch] for branch in branches] + [["Back"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Select a branch to add a record:", reply_markup=reply_markup)
    return BRANCH_NAME

# Add Record Branch Received
async def add_record_branch_received(update: Update, context: CallbackContext):
    """Ask for the product to add a record for."""
    if update.message.text.strip().lower() == "back":
        # If user selects "Back", go to the previous step
        await add_record_handler(update, context)
        return BRANCH_NAME
    
    context.user_data['branch_name'] = update.message.text.strip()
    branch_name = context.user_data['branch_name']
    data = load_data()
    products = list(data['branches'][branch_name]['inventory'].keys())
    
    if not products:
        await update.message.reply_text(f"No products found in {branch_name}. Create a product first.")
        return ConversationHandler.END
    
    # Add a "Back" button
    keyboard = [[product] for product in products] + [["Back"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Select a product to add a record:", reply_markup=reply_markup)
    return PRODUCT_NAME

# Add Record Product Received
async def add_record_product_received(update: Update, context: CallbackContext):
    """Ask for the date of the record."""
    if update.message.text.strip().lower() == "back":
        await add_record_branch_received(update, context)
        return BRANCH_NAME
    
    context.user_data['product_name'] = update.message.text.strip()
    await update.message.reply_text("Enter the date for the record (DD.MM.YYYY):")
    return RECORD_DATE

# Add Record Date Received
async def add_record_date_received(update: Update, context: CallbackContext):
    """Validate the date and ask again if it's incorrect."""
    if update.message.text.strip().lower() == "back":
        await add_record_product_received(update, context)
        return PRODUCT_NAME

    date_text = update.message.text.strip()

    # Try to parse the date
    try:
        record_date = datetime.datetime.strptime(date_text, "%d.%m.%Y")
        context.user_data['record_date'] = record_date.strftime("%d.%m.%Y")
        
        await update.message.reply_text("Enter the quantity of the product:")
        return RECORD_QUANTITY
    except ValueError:
        await update.message.reply_text(
            "Invalid date format! Please enter a valid date in the format DD.MM.YYYY."
        )
        return RECORD_DATE  # Stay in the same state to ask again

# Add Record Quantity Received
async def add_record_quantity_received(update: Update, context: CallbackContext):
    """Ask for attendance of specific branch's employees."""
    if update.message.text.strip().lower() == "back":
        await add_record_date_received(update, context)
        return RECORD_DATE
    
    context.user_data['record_quantity'] = int(update.message.text.strip())
    await update.message.reply_text("Enter employees' code who are present: ")
    return EMP_ATTENDANCE

# Add Record Attendance Received
async def add_record_attendance_received(update: Update, context: CallbackContext):
    """Add the record to the product."""
    if update.message.text.strip().lower() == "back":
        await add_record_quantity_received(update, context)
        return RECORD_QUANTITY
    
    data = load_data()
    
    branch_name = context.user_data['branch_name']
    product_name = context.user_data['product_name']
    record_date = context.user_data['record_date']
    record_quantity = context.user_data['record_quantity']
    input_emp_attendance = update.message.text.strip()

    # employee codes
    emp_code = data['branches'][branch_name]['employees']

    if input_emp_attendance == 'ev': 
        emp_attendance = list(emp_code)
    else: 
        employee_keys = input_emp_attendance.split()
        emp_attendance = [key for key in employee_keys if key in emp_code]

    success, message = add_record(branch_name, product_name, record_quantity, record_date, emp_attendance)

    await update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END



# # List Records Command
# async def list_records(update: Update, context: CallbackContext):
#     """Ask for the squad to list records."""
#     data = load_data()
#     squads = [squad for squad in data['employees']]
    
#     if not squads:
#         await update.message.reply_text("No squads found.")
#         return ConversationHandler.END
    
#     keyboard = [[squad] for squad in squads]
#     reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
#     await update.message.reply_text("Select a squad to list product records:", reply_markup=reply_markup)
#     return SQUAD_NAME

# async def list_records_squad_received(update: Update, context: CallbackContext):
#     """List the product records for the selected squad."""
#     squad_name = update.message.text.strip()
#     data = load_data()
    
#     if squad_name not in data['inventory'] or not data['inventory'][squad_name]:
#         await update.message.reply_text(f"No records found for {squad_name}.")
#         return ConversationHandler.END
    
#     records = data['inventory'][squad_name]
#     record_list = "\n".join([f"Date: {date}\nRecords: {', '.join(items)}\n\n" for date, items in records.items()])
#     await update.message.reply_text(f"Product records for {squad_name}:\n\n{record_list}")
#     return ConversationHandler.END

