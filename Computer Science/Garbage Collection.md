#MemoryManagement

- 變數的名稱與值都會佔用記憶體，所以沒用到的變數要記得將記憶體釋出，否則就是在浪費有限的記憶體空間，這種「無用的資料佔用記憶體」的現象又叫 **memory leak**
- Garbage collection 簡稱 GC，是一套檢查出沒用到的記憶體空間並將他們重新釋出的機制
- 大多數高階程式語言都有實作 GC
    - 開發者不太須要擔心 memory leak
    - 但有時候還是會有 GC 處理不了的問題
- C 與 C++ 都沒有 GC，所以開發者須要手動釋出記憶體

# GC 的策略

GC 的策略有很多，主流的兩種分別是 map and sweep 與 reference counting

### Map and Sweep

JavaScript 使用的是這種策略。

#TODO

### Reference Counting

下面示範在 Python 中如何取得一個物件的 reference counting：

```Python
import sys

a = []
b = a
print(sys.getrefcount(a)) # 3
```

上例中，list object 被 reference 三次，分別是 `a`, `b` 以及傳入 `sys.getrefcount` 的參數。

#TODO

# GC 如何分辨 Heap 中的資料是 Pointer 還是 Data？

### Tagged Pointers

在每個資料的最後加一個 bit，用這個 bit 來區分是 pointer 還是 data。

#TODO 
