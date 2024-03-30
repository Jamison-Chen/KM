# 原理

用一個 [[Higher-Order Function (HOF)]]「加工」其他 function，並使用 `@` 語法糖 (Syntax Sugar)，將 decorator 置於 function 定義的頂端。

==只有把 function 視為一等公民的程式語言，才「可能」有 decorator==。

舉例：

```Python
def print_function_name(func):
    def wrapper(*arg, **args):
        print("Use" + func.__name__)
        return func(*arg, **args)
    return wrapper

@print_function_name
def function_a(s: str):
    print(s)

function_a("ABC")

# Use function_a
# ABC
```

Decorator 中通常會有一個名為 wrapper 的 function，wrapper 會 return 原 function，return 原 function 前所做的事就是這個 decorator 的主要任務，而 wrapper 本身則是會被 decorator reutn 出去。

>[!Note]
>
>`wrapper` function 是 return 原 function (`func`) 填入參數後的執行結果 (`return func(*arg, **args)`)。
>
>Decorator 是 return `wrapper` 這個 function 而非 `wrapper` function 的執行結果，所以不用加括號。

如果不使用 `@print_function_name` 裝飾 `function_a`，也可以直接 call 兩層 function 來達到相同的效果，只是 call function 時就長得比較醜：

```Python
def print_function_name(func):
    def wrapper(*arg, **args):
        print("Use" + func.__name__)
        return func(*arg, **args)
    return wrapper

def function_a():
    print("A")

print_function_name(function_a)()
```

# Chaning Decorators

e.g.

```Python
# ...

@decorator_a
@decorator_b
def function_a():
    ...
```

在上例中，`function_a` 會先被 `decorator_b` 吃進去然後吐出來，再被 `decorator_a` 吃進去然後吐出來。

# 讓 Decorator 吐出的 Function 與原 Function 同名

方法：在 `return wrapper` 之前加上一行 `wrapper.__name__ = func.__name__`。

```Python
def decorator_a(func):
    def wrapper(*arg, **args):
        ...
        return func(*arg, **args)
    wrapper.__name__ = func.__name__
    return wrapper
```

# Decorator with Parameters

方法：需要在原本的 decorator 外多用一層 function 包住並 return decorator。

此時會將原本 decorator 的名字讓給包住 decorator 的那層函示，decorator 則改名為 `decorator` 即可。

舉例：

```Python
def print_function_name(capitalized:bool):
    def decorator(func):
        def wrapper(*arg, **args):
            if capitalized:
                print("Use" + func.__name__.upper())
            else:
                 print("Use" + func.__name__)
            return func(*arg, **args)
        return wrapper
    return decorator

@print_function_name(capitalized=True)
def function_a(s:str):
    print(s)

function_a("ABC")

# Output:
# Use FUNCTION_A
# ABC
```

使用 Decorator 時，一定要用 keyword argument 的方式設定參數。

# 使用 Decorator 替原 Function 加上其他可呼叫的 Attributes

>[!Note]
>此處有使用到 [[Python 中的 Closure 與 Captured Variable]] 的觀念。

有時候 decorator 的目的在於替原 function 統計一些數據（比如計算花了多少時間執行 function），因此 decorator 內部就會需要定義一些變數來做統計，而實際執行被裝飾的 function 後，要如何取得那些統計數據呢？

e.g.

```Python
def timer(func):
    from time import time
    
    timer = 0
    
    def time_spent():
        nonlocal timer
        return timer

    def wrapper(*arg, **args):
        nonlocal timer
        
        start = time()
        result = func(*arg, **args)
        timer = time() - start
        return result

    wrapper.time_spent = time_spent
    wrapper.__name__ = func.__name__

    return wrapper

@timer
def function_a():
    ...

function_a()
print(function_a.time_spent())
```

* 在 `timer` function 內定義一個變數 `timer`
* 定義一個 return `nonlocal` 變數 (captured variable) `timer` 的 `time_spent` function
* 在 `wrapper` function 中可以更動 `nonlocal` 變數 (captured variable) `timer` 的值
* 定義 `wrapper.time_spent = time_spent`
* 呼叫被裝飾的 function: `function_a` 後，可以呼叫 `function_a.time_spent()`

>[!Note]
>在上例中，定義一個「回傳 `nonlocal` 變數 (captured variable) `timer` 的 `time_spent` function」是必要的動作，不可以直接寫 `wrapper.time_spent = timer`，因為這樣得到的 `timer` 不是 captured variable，但 `wrapper` 中更動的是 captured variable。

##### 錯誤示範

```Python
def timer(func):
    from time import time
    
    timer = 0
    
    def wrapper(*arg, **args):
        nonlocal timer
        
        start = time()
        result = func(*arg, **args)
        timer = time() - start
        return result

    wrapper.timer = timer
    wrapper.__name__ = func.__name__

    return wrapper

@timer
def function_a():
    ...

function_a()
print(function_a.timer)  # 0
```

上述程式碼執行後，你會發現無論 `function_a` 花了多久執行，只會印出 `0`。

# Class-Based Decorator

可能有人會覺得上面這個正確做法有點醜，又要使用 `nonlocal`，又要使用回傳 nonlocal variable 的 function。其實有一個替代方案，就是使用 class-based decorator。

我們嘗試建構一個功能與上一段的 `timer` decorator 一樣的 `Timer` class decorator：

```Python
from time import time

class Timer:
    def __init__(self, func):
        self.time_spent = 0
        self.original_func = func
    
    def __call__(self, *arg, **args):
        start = time()
        result = self.original_func(*arg, **args)
        self.time_spent = time() - start
        return result

@Timer
def function_a():
    ...

function_a()
print(function_a.time_spent)
```

如此一來就不須要用到 `nonlocal`，也不須要 call function 才能取得 class 內的 attribute 了。
