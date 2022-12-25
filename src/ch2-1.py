from concurrent.futures import ThreadPoolExecutor as Executor
import time


def worker(data, num):
    """data should not be global variable"""
    data.append(num)
    time.sleep(1)


if __name__ == "__main__":
    data = []
    with Executor(max_workers=10) as exe:
        for i in range(10):
            future = exe.submit(worker, data, i)
            print(data)
    print("===")
    print(data)
