# Threading

e.g.

```Python
from threading import Thread

def threading(func, n: int, thread_count: int):
    threads = []
    for i in range(thread_count):
        # 將 n 個任務平分給每個 thread
        threads.append(Thread(target=func, args=(n // thread_count,)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def test(n: int) -> None:
    for i in range(n):
        i**0.5

if __name__ == "__main__":
    threading(test, 60000000, thread_count=6)
```

### Python 無法透過 Threading 加速運算

一般而言，multi-threaded program 都會使用到多個 CPU cores，從而加快運算速度，然而 Python 中有 [[GIL]]，這使得 Python interpreter 在一個時間點只能執行一個 thread，所以即使使用 threading， Python 也無法真正地「平行」運算，只能在多個 threads 間進行切換，達到 [[Operating System/零碎筆記#Concurrency vs. Parallelism|Concurrency]] 的效果，運算速度也就不會變快。

在上面的例子中，執行 `threading(test, 60000000, thread_count=6)` 與直接執行 `test(60000000)` 所花的時間幾乎是一樣的。

# Multi-processing

#TODO

# 參考資料

- <https://www.youtube.com/watch?v=AZnGRKFUU0c>
- <https://www.youtube.com/watch?v=X7vBbelRXn0>
