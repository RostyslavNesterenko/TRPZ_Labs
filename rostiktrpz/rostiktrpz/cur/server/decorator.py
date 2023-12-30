import time


def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"Виконання операції '{func.__name__}'...")
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Операція '{func.__name__}' виконалася за {execution_time:.4f} секунди.")

        return result
    return wrapper