def main():
    """Start the bot and handle all commands."""
    application = Application.builder().token("6678455810:AAER7grRqqBQQpbGFzwu8s0b5yqSQPJCvb0").build()

    # Conversation handlers
    squad_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create_squad', create_squad)],
        states={SQUAD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, squad_name_received)]},
        fallbacks=[]
    )

    delete_branch_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('delete_branch', delete_branch)],
        states={SQUAD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_squad_received)]},
        fallbacks=[]
    )
    
    add_employee_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add_employee', add_employee)],
        states={
            SQUAD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_employee_squad_received)],
            EMPLOYEE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_employee_name_received)],
            EMPLOYEE_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_employee_code_received)]
        },
        fallbacks=[]
    )
    
    remove_employee_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('remove_employee', remove_employee)],
        states={
            SQUAD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_employee_squad_received)],
            EMPLOYEE_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_employee_code_received)]
        },
        fallbacks=[]
    )
    
    list_employees_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('list_employees', list_employees)],
        states={SQUAD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, list_employees_squad_received)]},
        fallbacks=[]
    )

    create_product_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create_product', create_product)],
        states={
            SQUAD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_product_squad_received)],
            PRODUCT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_product_name_received)]
        },
        fallbacks=[]
    )

    add_record_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add_record', add_record)],
        states={
            SQUAD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_record_squad_received)],
            PRODUCT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_record_product_received)],
            PRODUCT_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_record_date_received)],
            PRODUCT_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_record_quantity_received)]
        },
        fallbacks=[]
    )

    list_records_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('list_records', list_records)],
        states={SQUAD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, list_records_squad_received)]},
        fallbacks=[]
    )

   

    # Command Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(squad_conv_handler)
    application.add_handler(delete_squad_conv_handler)
    application.add_handler(CommandHandler('list_squads', list_squads))
    application.add_handler(add_employee_conv_handler)
    application.add_handler(remove_employee_conv_handler)
    application.add_handler(list_employees_conv_handler)
    application.add_handler(create_product_conv_handler)
    application.add_handler(add_record_conv_handler)
    application.add_handler(list_records_conv_handler)

    # Start polling
    application.run_polling()

if __name__ == '__main__':
    main()




async def record_date_received(update: Update, context: CallbackContext):
    """Validate the date and ask again if it's incorrect."""
    date_text = update.message.text.strip()

    # Try to parse the date
    try:
        record_date = datetime.datetime.strptime(date_text, "%d.%m.%Y")
        context.user_data['record_date'] = record_date
        await update.message.reply_text(f"Date {date_text} is valid.")
        
        # Proceed to the next step (e.g., record quantity or something else)
        # return NEXT_STATE  # Update this line with your next state
    except ValueError:
        # If the date is invalid, ask the user to re-enter
        await update.message.reply_text(
            "Invalid date format! Please enter a valid date in the format DD.MM.YYYY."
        )
        return RECORD_DATE  # Stay in the same state to ask again
    

async def add_record_date_received(update: Update, context: CallbackContext):
    """Ask for the quantity of the product."""
    context.user_data['record_date'] = update.message.text.strip()
    await update.message.reply_text("Enter the quantity of the product:")
    return RECORD_QUANTITY