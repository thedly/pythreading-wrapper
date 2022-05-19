from pytest import fixture

from ThreadingWrapper.concurrency import FunctionArgs, MultiThreading

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def chunk(start: int, end: int):
    return data[start:end]


@fixture()
def threading():
    mt = MultiThreading()
    return mt


def test_execute_async(threading):
    args = [FunctionArgs(chunk, output_var='', start=item, end=item+2) for item in range(0, 10, 2)]
    op: list = threading.execute_by_chunks_async(*args)
    print(op)
    assert data[1] in op
    assert data[3] in op
    assert data[5] in op
    assert data[7] in op
