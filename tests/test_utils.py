def check_error_message(context, message) -> bool:
    return message in str(context.exception)
