# Threading

舉例：

```Python
def threading(func, n:int, thread_count:int):
    from threading import Thread

    threads = []

    for i in range(thread_count):
        # 將 `n` 個任務分成 `thread_count` 份，依序丟給每個 `Thread` 中的 `func`
        threads.append(Thread(target=func, args=(n // thread_count,)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def test(n: int):
    for i in range(n):
        i**0.5

if __name__ == "__main__":
    threading(test, 60000000, thread_count=6)
```

Python 中有 [[GIL]] 機制，這使得 Python Interpreter 在一個時間點只能執行一個 thread。運行 multithread 程式時， Python 並無法真正的平行運算，只能在多個 threads 間進行 context switching，達到 [[Operating System/零碎筆記#Concurrency vs. Parallelism|Concurrency]] 的效果。

也就是說在 Python 中使用 threading 並不會加快運算速度，在上面的例子中，執行 `threading(test, 60000000, thread_count=6)` 與直接執行 `test(60000000)` 所花的時間幾乎是一樣的。

#TODO

# Multi-processing

#TODO

# 參考資料

<https://www.youtube.com/watch?v=AZnGRKFUU0c>

<https://www.youtube.com/watch?v=X7vBbelRXn0>
