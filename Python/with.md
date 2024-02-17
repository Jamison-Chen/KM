認識 `with` statement 前一定要先認識 context manager object。
# Context Managers

Context manager object 是一種必須擁有 `__enter__` 和 `__exit__` 兩個 methods 的 object，這兩個 methods 扮演著「入口」和「出口」的角色。

搭配 `with` statement 使用的效果就是，一進入 `with` block，首先 context manager object 的 `__enter__` method 就會被觸發，離開 `with` block 前的最後一件事則是觸發 `__exit__` method。

所以如果有什麼事情是在執行某段程式碼前一定要做的，或者有什麼事情是在執行完某段程式碼後一定要做的，就可以使用 context manager object 將那些一定要做的事抽離出來。

某種程度上，使用 context manager 可以避免開發者忘記做一些瑣碎卻必要的事，比如關閉檔案、將某些臨時更動的系統全域變數改回預設值… 等。

# 使用範例

實務上最常用到 `with` statement 就是在讀寫檔案時，由於讀寫檔案前一定要將檔案先打開，讀寫完後一定要將檔案關起來，一般人可能不會忘記要打開檔案才能讀，但卻很有可能在讀寫完檔案後忘了將它關起來，這時候就是 `with` statement 可以派上用場的時候了。

在沒有 `with` statement 的時代，你可能會這樣讀寫檔案：

```Python
file = open("file_path", "w")
file.write("Hello")
file.close()
```

稍微有經驗一點後，你知道有可能 write 會噴錯，導致沒有 close，所以可能會改成這樣：

```Python
file = open("file_path", "w")
try:
    file.write("Hello")
finally:
    file.close()
```

有了 `with` statement 後，會變成這樣：

```Python
with open("file_path", "w") as file:
    file.write("Hello")
```

# 當 raise Exception 時

如果在 `with` block 中的程式丟出 exception，在離開 `with` block 前還是會呼叫 context manager object 的  `__exit__` method，也就是說其實 `with` statement 有一部份是由 `try...except...finally..` 構成的。

下方程式碼：

```Python
with EXPRESSION as TARGET:
    SUITE
```

的執行結果會等同於：

```Python
manager = ...  # EXPRESSION
enter = type(manager).__enter__
exit = type(manager).__exit__
value = enter(manager)
hit_except = False

try:
    TARGET = value
    SUITE
except:
    hit_except = True
    if not exit(manager, *sys.exc_info()):
        raise
finally:
    if not hit_except:
        exit(manager, None, None, None)
```

# 自己寫一個 Context Manager

### Class-Based Context Manager

一個 context manager class 的 template 會長得像這樣：

```Python
class MyContextManager:
    def __init__(self, *args, **kwargs):
        ...
        
    def __enter__(self):
        ...
        
    def __exit__(self, exception_type, exception_val, traceback):
        ...
        
```

假設你現在想要在準備執行一段程式碼前先印出 "start"，執行完該段程式碼後印出 "end"，那你可以這樣寫：

```Python
class MyContextManager:
    def __init__(self):
        ...
        
    def __enter__(self):
        print("start")
        
    def __exit__(self, exception_type, exception_val, traceback):
        print("end")

with MyContextManager():
    for i in range(3):
        print(i)

# Output:
# start
# 0
# 1
# 2
# end
```

在 `with EXPRESSION as TARGET:...` 的語法中，`TARGET` 就是 `__enter__` method 的回傳值。比如我現在想要一個 Dog 可以在進入 `with` block 時誕生並在離開 `with` block 前睡著的功能：

```Python
class MyContextManager:
    def __init__(self):
        self.dog = None
        
    def __enter__(self):
        self.dog = Dog("Lucky")
        return self.dog
        
    def __exit__(self, exception_type, exception_val, traceback):
        self.dog.sleep()

with MyContextManager() as d:
    d.bark()
```

如果我還想在那隻狗誕生前先為他取好名字：

```Python
class MyContextManager:
    def __init__(self, name:str):
        self.dog = None
        self.name = name
        
    def __enter__(self):
        self.dog = Dog(name=self.name)
        return self.dog
        
    def __exit__(self, exception_type, exception_val, traceback):
        self.dog.sleep()

with MyContextManager("Jasper") as d:
    d.bark()
```

### Function-Based Context Manager

如果你回頭看前面讀寫檔案的例子，應該會發現：`with open("file_path")` 的 `open` 看命名方式感覺不像是一個 class 的名稱，反而像是一個 function，難道是命名錯誤嗎？

其實 `open` 真的是一個 function，context manager 除了以 class 的方式被建立，也可以用 function 來建構，Python 標準函式庫提供了 `contextlib` module，只要為 function 加上 `contextlib.contextmanager` [[Decorator]]，就可以讓 function 成為 context manager。

一樣以 Dog 為例：

```Python
from contextlib import contextmanager

@contextmanager
def my_context_manager(name:str):
    try:
        dog = Dog(name=name)
        yield dog
    finally:
        dog.sleep()

with my_context_manager("Jasper") as d:
    d.bark()
```

定義 function-based context manager 時，有以下幾點須注意：

- 一定要用 `try...except...finally` statement，其中 `except` statement 可視情況省略，`finally` 則一定要有
- `finally` block 扮演的角色其實就是 class-based context manager 的 `__exit__` method
- `try` block 裡是使用 `yield` 語法回傳 `with EXPRESSION as TARGET:...` 的語法中的 `TARGET`

    這裡不能用 `return`（關於 `yield` 的用法詳見 [[Generator and the yield Statement]]），因為相較於 `return` 會直接跳出並結束 function，`yield` 回傳值時則是讓 function「暫停」，這樣在跳出 `with` block 時才會回到上次暫停的地方繼續運行完剩下的 `finally` block。

功能簡單的 context manager 有時候其實不一定要寫成一個 class。

# 簡化巢狀的 `with` statements

當需要兩個以上的 context managers 時，最直覺的方法可能是巢狀地撰寫：

```Python
with A() as a:
    with B() as b:
        SUITE
```

但其實你也可以一層解決：

```Python
with A() as a, B() as b:
    SUITE
```

如果為了程式易讀，也可以加上括號：

```Python
with (
    A() as a,
    B() as b,
):
    SUITE
```

# 參考資料

###### 官方

- <https://docs.python.org/3/reference/compound_stmts.html#the-with-statement>
- <https://docs.python.org/3/reference/datamodel.html#context-managers>

###### 非官方

- <https://builtin.com/software-engineering-perspectives/what-is-with-statement-python>
