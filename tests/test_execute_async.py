import time

from pytest import fixture

from ..ThreadingWrapper.concurrency import FunctionArgs, MultiThreading


def long_running_process(param1: int):
    time.sleep(1)
    return param1


@fixture()
def threading():
    mt = MultiThreading()
    return mt


def test_execute_async(threading):
    args = [FunctionArgs(long_running_process, output_var=item, param1=item) for item in range(5)]
    op: dict = threading.execute_async(*args)
    assert len(op.items()) == 5
    assert op[1] == 1
    assert op[2] == 2
    assert op[3] == 3
    assert op[4] == 4
