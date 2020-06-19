import contextvars

__version__ = "0.0.1"

db_ctx = contextvars.ContextVar('DB')
