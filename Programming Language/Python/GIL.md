GIL 是 Global Interpreter Lock 的縮寫。

# 為何需要 GIL

首先，Python 透過計算一塊記憶體空間的 [reference count](</Computer Science/Garbage Collection.md>) 來判斷該空間是否應該被釋出，而計算 reference count 時，應避免 [race condition](</Operating System/零碎筆記.md#Race Condition>)（多個 threads 同時更改同一個變數的 reference count，而導致某些更改沒有成功）否則就會有「不該被釋出的空間被釋出，進而導致 bug」或「該被釋出的空間沒有被釋出 (**Memory Leak**)」等現象。

透過 locks，可以使得沒有權限（或者說鑰匙）的 thread(s) 在某資料的 lock 解除前無法更改該資料（也就無法更改資料的的 reference），進而避免 race condition，但是若同時存在多個 locks 就有可能發生 [Deadlocks](</Operating System/Deadlocks.md>)，所以，GIL 的策略就是：

>只有一個 global lock，就可以同時避免 race condition 與 deadlocks。

# GIL 是雙面刃

由於只有一個 global lock，所以所有 Python bytecode 要被執行前就必須先取得 GIL 的權限，這使得：

>Python interpreter 在一個時間點只能執行一個 thread。

Python 於是成為少數「即使在 multi-threaded OS 架構下、同時搭載 multi-core CPU，也無法達到 parallel threading」的程式語言之一。

雖然不能平行運算，但還是可以看起來像是平行運算([concurrency](</Operating System/零碎筆記.md#Concurrency vs. Parallelism>))，但因為一個時間點只執行一個運算，所以==「是否採用 threading」對於「做完所有運算所花費的總時間」並不會有太大影響==。

一個簡單的實驗如下：

```Python
def test(n: int):
    for i in range(n):
        i**0.5

def threading(func, n:int, thread_count:int):
    from threading import Thread

    threads = []

    for i in range(thread_count):
        # 將 `n` 個任務分成 `thread_count` 份，依序丟給每個 `Thread` 的 `func`
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

GIL 的誕生是為了避免 race condition，而之所以要避免 race condition 是因為某些 interpreter 採用了 reference counting 來進行 memory management，但 memory management 本來就不止一種方法，[Garbage Collection](</Computer Science/Garbage Collection.md>) 就是另一個選項。總之，如果你想拋棄 GIL，那你就得先拋棄 reference counting。

最後還是幫 GIL 說句公道話，雖說 GIL 使得 Python 無法使用 multi-threading 進行平行運算，但由於只要管理一個 lock，GIL 其實加快了 single-threaded 的運算速度。

# 參考資料

- <https://realpython.com/python-gil/>
