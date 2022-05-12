import traceback
from wrappers import time_it
from models import FunctionArgs
from concurrent.futures import as_completed, ThreadPoolExecutor


class MultiThreading:

    __capacity: int

    def __init__(self, max_workers: int = None):
        self.__capacity = max_workers

    @time_it('execute_async')
    def execute_async(self, *functions: FunctionArgs) -> dict:
        result = dict()
        try:
            with ThreadPoolExecutor(max_workers=self.__capacity) as pool:
                tasks = {pool.submit(function.pointer, *function.arguments, **function.keyword_arguments):function for function in functions}

                for output in as_completed(tasks):
                    functionArgs = tasks[output]
                    try:
                        data = output.result()
                        result[functionArgs.output_var] = data
                    except Exception as exc:
                        print("exception occured while multiprocessing")
                        print(exc)
                        traceback.print_exc()
                    # else:
                    #     if data is not None:
                    #         print('loaded data of %d records' % (len(data)))
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

                for output in as_completed(tasks):
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
                        traceback.print_exc()
                    # else:
                    #     if data is not None:
                    #         #print('loaded data of %d records' % (len(data)))
            return result
        except Exception as ex:
            traceback.print_exc()
            raise