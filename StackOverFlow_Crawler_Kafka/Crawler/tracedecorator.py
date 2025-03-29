# tracedecorator.py

import inspect
from functools import wraps
from datetime import datetime
import os


def log_usage(log_file="usage.log"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = datetime.now().isoformat()
            # Determine caller name (using the class name or "Module")
            caller = args[0].__class__.__name__ if args and hasattr(
                args[0], '__class__') else "Module"
            params = inspect.signature(func).bind(*args, **kwargs).arguments

            def log(message):
                # Ensure that the new log entry starts on a new line
                if os.path.exists(log_file):
                    with open(log_file, "rb+") as f:
                        f.seek(0, os.SEEK_END)
                        if f.tell() > 0:  # Only if the file is not empty
                            f.seek(-1, os.SEEK_END)
                            last_char = f.read(1)
                            if last_char != b"\n":
                                f.write(b"\n")
                # Write the actual log message followed by a newline.
                with open(log_file, "a") as f:
                    f.write(message + "\n")

            log(f"{current_time} | ENTER {caller}.{func.__qualname__} |"
                # f"Params: {params}"
                )

            try:
                result = func(*args, **kwargs)
            except KeyboardInterrupt:
                log(f"{datetime.now().isoformat()} | INTERRUPTED {caller}.{func.__qualname__}")
                raise
            except Exception as e:
                log(f"{datetime.now().isoformat()} | ERROR {caller}.{func.__qualname__} | {type(e).__name__}: {e}")
                raise

            log(f"{datetime.now().isoformat()} | EXIT {caller}.{func.__qualname__}")
            return result

        return wrapper
    return decorator
