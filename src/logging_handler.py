import logging


class CallbackHandler(logging.Handler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def emit(self, record):
        # 'record' is the LogRecord object.
        # You can access .msg, .levelname, .created, etc.

        # Format the message using the standard formatter (if one is set)
        log_entry = self.format(record)

        # Trigger your hook
        try:
            self.callback(log_entry)
        except Exception:
            # Important: Handle errors in your hook so logging doesn't crash the app
            self.handleError(record)
