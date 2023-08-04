GIL 是 Global Interpreter Lock 的縮寫。

# 為何需要 GIL

首先，Python 透過計算一塊記憶體空間的 [[Garbage Collection vs. Reference Counting|reference count]] 來判斷該空間是否應該被釋出，而計算 reference count 時，應避免 [[Operating System/零碎筆記#Race Condition|Race Condition]]（多個 threads 同時更改同一個變數的 reference count，而導致某些更改沒有成功）否則就會有「不該被釋出的空間被釋出，進而導致 bug」或「該被釋出的空間沒有被釋出 (Memory Leak)」等現象。

透過 locks，可以使得沒有權限（或者說鑰匙）的 thread(s) 在某資料的 lock 解除前無法更改該資料（也就無法更改資料的的 reference），進而避免 Race Condition，但是若同時存在多個 locks 就有可能發生 [[Deadlocks (死結)]]，所以，GIL 的策略就是：

>只有一個 Global lock，就可以同時避免 Race Condition 與 Deadlocks。

# GIL 是雙面刃

由於只有一個 Global lock，所以所有 Python bytecode 要被執行前就必須先取得 GIL 的權限，這使得：

>Pyhton Interpreter 在一個時間點只能執行一個 thread。

Python 於是成為少數「即使在 Multi-threaded OS 架構下，同時搭載 multi-core CPU，也無法達到 Parallel Threading」的程式語言之一。

雖然不能平行運算，但還是可以看起來很像是平行運算，也就是說 Python 中的 threading 可以做到 [[Operating System/零碎筆記#Concurrency vs. Parallelism|Concurrency]]，但因為一個時間點只執行一個運算，所以「是否採用 threading」對於「做完所有運算所花費的總時間」並不會有太大影響。

一個簡單的實驗如下：

```Python
def test(n: int):
    for i in range(n):
        i**0.5

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
    # Without threading
    test(60000000)

    # With 6 threads
    threading(test, 60000000, thread_count=6)
```

用我的電腦執行上例中的 `test(60000000)` 以及 `threading(test, 60000000, thread_count=6)` 各自都花了約 4.3 秒。

# 不一定要用 GIL

GIL 的誕生是為了避免 Race Condition，而之所以要避免 Race Condition 是因為某些 Interpreter 採用了 reference counting 來進行 memory management，但 memory management 本來就不止一種方法，[[Garbage Collection vs. Reference Counting|Garbage Collection]] 就是另一個選項。總之，如果你想拋棄 GIL，那你就得先拋棄 reference counting。

最後還是幫 GIL 說句公道話，雖說 GIL 使得 Python 無法使用 threading 進行平行運算，但由於只要管理一個 lock，GIL 其實加快了 Single-threaded 的運算速度。

# 參考資料

<https://realpython.com/python-gil/>
