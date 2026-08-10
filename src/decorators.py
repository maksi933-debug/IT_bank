import functools
from typing import Callable, Optional, ParamSpec, TypeVar

# Переменные типов для сохранения сигнатуры декорируемой функции
P = ParamSpec("P")
R = TypeVar("R")


def log(filename: Optional[str] = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Декоратор, который логирует работу функции.
    Результат записывается в файл (если указан filename) или выводится в консоль.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"

                # Вывод лога успешного выполнения
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)

                return result

            except Exception as e:
                # Форматирование сообщения об ошибке с входными параметрами
                error_message = f"{func.__name__} error: {type(e).__name__}. " f"Inputs: {args}, kwargs: {kwargs}"

                # Вывод лога ошибки
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message + "\n")
                else:
                    print(error_message)

                # Пробрасываем ошибку дальше, чтобы программа знала о сбое
                raise

        return wrapper

    return decorator
