from configurations.management import call_command


# wrapping `manage.py flushexpiredtokens`
def flush_expired_tokens_command():
    return call_command("flushexpiredtokens")
