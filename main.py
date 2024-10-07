from bot_token import TOKEN
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from bot_handlers import BRANCH_NAME, EMPLOYEE_NAME, EMP_ATTENDANCE, PRODUCT_NAME, RECORD_DATE, RECORD_QUANTITY
from bot_handlers import start, create_branch_handler, branch_name_received, delete_branch_handler, delete_branch_received, list_branches_handler
from bot_handlers import add_employee_handler, add_employee_branch_received, add_employee_name_received, remove_employee_handler, remove_employee_branch_received, remove_employee_name_received
from bot_handlers import create_product_handler, create_product_branch_received, create_product_name_received
from bot_handlers import add_record_handler, add_record_branch_received, add_record_product_received, add_record_date_received, add_record_quantity_received, add_record_attendance_received
from bot_handlers import calculate_salary_handler, calculate_salary_branch_received

def main():
    """Start the bot and handle all commands."""
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler('start', start))

    # Conversation handlers for squad creation
    create_branch_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create_branch', create_branch_handler)],
        states={BRANCH_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, branch_name_received)]},
        fallbacks=[]
    )

    delete_branch_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('delete_branch', delete_branch_handler)],
        states={BRANCH_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_branch_received)]},
        fallbacks=[]
    )

    list_branches_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('list_branches', list_branches_handler)],
        states={BRANCH_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, list_branches_handler)]},
        fallbacks=[]
    )

    add_employee_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add_employee', add_employee_handler)],
        states = {
            BRANCH_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_employee_branch_received)],
            EMPLOYEE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_employee_name_received)]
        },
        fallbacks=[]
    )

    remove_employee_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('remove_employee', remove_employee_handler)],
        states={
            BRANCH_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_employee_branch_received)],
            EMPLOYEE_NAME: [MessageHandler(filters.TEXT & ~ filters.COMMAND, remove_employee_name_received)]
        },
        fallbacks=[]
    )

    create_product_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create_product', create_product_handler)], 
        states={
            BRANCH_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_product_branch_received)],
            PRODUCT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_product_name_received)]
        },
        fallbacks=[]
    )

    add_record_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add_record', add_record_handler)],
        states={
            BRANCH_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_record_branch_received)],
            PRODUCT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_record_product_received)],
            RECORD_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_record_date_received)],
            RECORD_QUANTITY: [MessageHandler(filters.TEXT  & ~filters.COMMAND, add_record_quantity_received)],
            EMP_ATTENDANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_record_attendance_received)]
        },
        fallbacks=[]
    )

    calculate_salary_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('calculate_salary', calculate_salary_handler)],
        states={
            BRANCH_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, calculate_salary_branch_received)]
        },
        fallbacks=[]
    )
    

    # Add conversation handlers to current application 
    application.add_handler(create_branch_conv_handler)
    application.add_handler(delete_branch_conv_handler)
    application.add_handler(list_branches_conv_handler)
    application.add_handler(add_employee_conv_handler)
    application.add_handler(remove_employee_conv_handler)
    application.add_handler(calculate_salary_conv_handler)
    application.add_handler(create_product_conv_handler)
    application.add_handler(add_record_conv_handler)
    


    # Start polling
    application.run_polling()

if __name__ == '__main__':
    main()

