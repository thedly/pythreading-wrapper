from concurrent.futures import ThreadPoolExecutor, as_completed

from .decorators import time_it
from .models import FunctionArgs

class MultiThreading:

    __capacity: int
    __timeout: float

    def __init__(self, max_workers: int = 60, timeout = 60):
        self.__capacity = max_workers
        self.__timeout = timeout

    @time_it('execute_async')
    def execute_async(self, *functions: FunctionArgs) -> dict:
        result = dict()
        try:
            with ThreadPoolExecutor(max_workers=self.__capacity) as pool:
                tasks = {pool.submit(function.pointer, *function.arguments, **
                                     function.keyword_arguments): function for function in functions}

                for output in as_completed(tasks, timeout=self.__timeout):
                    functionArgs = tasks[output]
                    try:
                        data = output.result()
                        result[functionArgs.output_var] = data
                    except Exception as exc:
                        print("exception occured while multiprocessing")
                        print(exc)
            return result
        except Exception as ex:
            print(ex)
            raise

    @time_it('execute_by_chunks_async')
    def execute_by_chunks_async(self, *functions: FunctionArgs) -> list:
        result = []
        try:
            with ThreadPoolExecutor(max_workers=self.__capacity) as pool:
                tasks = {pool.submit(function.pointer, *function.arguments, **function.keyword_arguments): function for
                         function in functions}

                for output in as_completed(tasks, timeout=self.__timeout):
                    try:
                        data = output.result()
                        if data is None:
                            print("no data available")
                            print(data)
                        else:
                            result.extend(data)
                    except Exception as exc:
                        print("exception occured while multiprocessing")
                        print(exc)
            return result
        except Exception as ex:
            print(ex)
            raise
