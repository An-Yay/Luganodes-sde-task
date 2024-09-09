import time


def retry(max_attempts=3, delay=5):
 
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt == max_attempts:
                        raise e
                    time.sleep(delay)
        return wrapper
    return decorator
