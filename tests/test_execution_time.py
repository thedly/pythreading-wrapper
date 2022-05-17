import time

from pytest import fixture

from ..src.concurrency import FunctionArgs, MultiThreading

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def chunk(start: int, end: int):
    time.sleep(1)
    return data[start:end]


@fixture()
def threading():
    mt = MultiThreading()
    return mt


def long_running_process(param1: int):
    time.sleep(1)
    return param1


def test_execute_by_chunks_async_duration(threading):

    start_slow_execution = time.time()
    items = []
    for count in range(0, 10, 2):
        items.extend(chunk(start=count, end=count+2))
    end_slow_execution = time.time()
    slow_execution_time = end_slow_execution - start_slow_execution
    print('slow_execution_time', slow_execution_time)
    start_fast_execution = time.time()
    args = [FunctionArgs(chunk, output_var='', start=item, end=item+2) for item in range(0, 10, 2)]
    op: list = threading.execute_by_chunks_async(*args)
    end_fast_execution = time.time()
    fast_execution_time = end_fast_execution - start_fast_execution
    print('fast_execution_time', fast_execution_time)

    assert fast_execution_time < slow_execution_time
    assert len(op) == len(items)


def test_execute_async_duration(threading):

    start_slow_execution = time.time()
    items = {}
    for count in range(5):
        items[count] = long_running_process(count)
    end_slow_execution = time.time()
    slow_execution_time = end_slow_execution - start_slow_execution
    print('slow_execution_time', slow_execution_time)

    start_fast_execution = time.time()

    args = [FunctionArgs(long_running_process, output_var=item, param1=item) for item in range(5)]
    op: dict = threading.execute_async(*args)

    end_fast_execution = time.time()
    fast_execution_time = end_fast_execution - start_fast_execution
    print('fast_execution_time', fast_execution_time)
    assert fast_execution_time < slow_execution_time
    assert len(op.keys()) == len(items.keys())
