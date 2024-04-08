Python Interpreter 預設的 recursion depth 的極限為 1000，分別有 getter function 與 setter function 可以取得這個值以及設定這個值：

```Python
import sys

print(sys.getrecursionlimit()) # 1000

# 使用 `sys.setrecursionlimit()` 更改這個預設值：
sys.setrecursionlimit(2000)

print(sys.getrecursionlimit()) # 2000
```

# Recursion Error

當一個 recursive function 的遞迴深度超過限制時會報錯：

e.g.

```Python
def fibonacci(n):
    if n <= 1:
        return n
    return(fibonacci(n-1) + fibonacci(n-2))

print(fibonacci(1000))
```

Output:

```plaintext
RecursionError: maximum recursion depth exceeded while calling a Python object
```

# 暫時更改 Recursion Depth Limit

```Python
import sys

class recursion_depth:
    def __init__(self, limit):
        self.limit = limit
        self.default_limit = sys.getrecursionlimit()
    
    def __enter__(self):
        sys.setrecursionlimit(self.limit)
    
    def __exit__(self, type, value, traceback):
        sys.setrecursionlimit(self.default_limit)

with recursion_depth(2000):
    print(fibonacci(1000))
```

這個方法可以確保只有在 `with` block 內， recurision limit 才是指定的數量，脫離 `with` block 後，recurision 便會變回預設的 1000，避免開發者不小心永久更改到系統的設定。

>[!Info]
>關於 `with` 的用法，可以參考[[Context Manager & with|這篇]]。

### 過深的 Recursion Depth Limit 可能導致 Stack Overflow

由於每一次的 funciton call 在還沒 return 之前都會佔據 call stack 中一個位置，因此過深的 recursive funciton call 可能會導致 stack overflow。至於要多深導致 stack overflow，則取決於 OS 給的限制、目前剩多少 memory、interpreter 的種類（CPython vs. PyPy），以及 function 本身是否有再 call 其他 functions。
