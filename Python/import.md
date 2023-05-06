# `import` 如何運作？

一個最簡單的 `import` statement 可能長得如下：

```Python
import abc
```

Python interpreter 處理 `import` statement 的流程則如下：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/import flow 2.jpg>)

第一步的 `sys.modules` 扮演 module cache 的角色，值得注意的是，`sys.modules` 是可以被篡改的，有心人士可以透過竄改 module cache 讓 Python Interpreter 誤以為自己有或沒有 import 某個 package/module。

由上方的流程圖可以發現，因為是先查看標準函式庫再查詢 `sys.path`，所以當有三方或 local 的 package/module 與標準函式庫的 package/module 撞名時，只有標準函式庫的那份會被 import 進來。（但是如果你有用 absolute 或 relative 的方式 import 的話，系統就會跳過前兩個步驟，直接尋找你指定的 directory 是否存在這個 package/module）

# 各種 `import` 語法

### 一、`import XXX`

```Python
import abc
```

- XXX 可能是 package name 或 module name，範例中的 `abc` 是標準函式庫中的某個 package。
- 當 XXX 是 module name 時，那這個 module 一定與目前的檔案在同一個 directory 內。
- 其實 `import` <*package-name*> 真正 import 的是 package 中的 `__init__.py` 檔案。

### 二、`from XXX import YYY`

```Python
from datetime import time
```

- 有可能 XXX 是 package name 而 YYY 是 module name；或者 XXX 是 module name 而 YYY 是 objects name（object 可以是 funcion, class, variable 等）。
- XXX 可以透過 `.` 來表示「路徑的下一層」，但 YYY 不可以有 `.`。

### 三、取別名

無論是 `import XXX` 或 `from XXX import YYY` 都可以在 `import` 的東西後面加上 `as 別名` 。

```Python
from datetime import datetime as dt
```

# Absolute Imports

如果你 import local app package 或 module 時，是乖乖地從那個 package/module 所在的最上層 directory 開始寫，那麼你用的就是 absolute imports，absolute imports 是 PEP8 建議的 import 方式。

比如當你的 project 結構如下時：

```plaintext
└── project
    ├── package1
    │   ├── module1.py
    │   └── module2.py
    └── package2
        ├── __init__.py
        ├── module3.py
        ├── module4.py
        └── subpackage1
            └── module5.py
```

absolute imports 會長得像這樣：

```Python
from package1 import module1
from package1.module2 import function1
from package2 import class1
from package2.subpackage1.module5 import function2
```

# Relative Imports

雖然 absolute imports 是建議的寫法，但有時候鄰近的兩個 module 之間 import 還要寫完整個路徑感覺其實很蠢，比如如果在 /a/b/c/d/e 這個路徑下有個 `m1.py` 裡面想要 import 與自己在相同 directory 的 `m2.py` 檔案，如果使用 absolute import 就會是 `from a.b.c.d.e import m2`；如果是 relative import 就是：

```Python
from . import m2
```

同理，如果你想 import 上上一層（也就是 /a/b/c/d 這個路徑）底下的 `m3.py`，你可以這麼寫：

```Python
from .. import m3
```

# Circular Import Problem

簡言之，如果 `a.py` 與 `b.py` 互相 import 彼此，就「可能」會造成 circular import problem，注意，是可能，也就是說 circular import 其實並不是不可以的，只是需要用某些方式避免 cicular import problem。

最簡單的會造成 cicular import problem 的例子如下：

```Python
# a.py
import b

def say_hi_and_yes():
    b.say_hi()
    print("yes")

def say_no():
    print("no")

say_hi_and_yes()
```

```Python
# b.py
import a

def say_hi():
    print("hi")

def say_hello_and_no():
    print("hello")
    a.say_no
```

此時若執行 `a.py`，就會造成 circular import problem，原因是因為當 `a.py` import `b.py` 時，`b.py` 內的程式碼就會開始編譯並執行，執行完才算 import 完畢，而 `b.py` 首先執行的就是 `import a`， 感覺就要掉入無窮迴圈了，不過其實問題不是出在這，Python Interpreter 有做基本的防呆，不會就此掉入迴圈，而是會「假裝」`a.py` 已經 import 好 `b.py`了，然後繼續執行 `a.py` 後續的程式碼。真正的錯誤是發生在 `a.py` 執行到 `say_hi_and_yes()` 時，因為剛剛「假裝 Import 好了」，其實 `b.py` 中的 `say_hi` function 根本還沒被編譯到，於是就會跳出以下 Error:

```plaintext
AttributeError: partially initialized module 'b' has no attribute 'say_hi' (most likely due to a circular import)
```

避免 cicular import problem 的方法之一，就是在 `a.py` 中 `b.say_hi()` 這段程式碼放入 [[if __name__ == "__main__" 是什麼|`if __name__ == "__main__":`]] 這樣的 block 中：

```Python
# a.py
import b

def say_hi_and_yes():
    b.say_hi()
    print("yes")

def say_no():
    print("no")

if __name__ == "__main__":
    say_hi_and_yes()
```

第二種方法，就是在 function 中再 import 必要的資源：

```Python
# a.py
def say_hi_and_yes():
    import b
    
    b.say_hi()
    print("yes")

def say_no():
    print("no")

say_hi_and_yes()
```

```Python
# b.py
def say_hi():
    print("hi")

def say_hello_and_no():
    import a
    
    print("hello")
    a.say_no
```

# PEP8 建議的 `import` 風格

1. `import` 最好寫在一個檔案的最前面（為了防止 circular import problem 者則不在此限），但要在 docstring 後面
2. `import` 最好依「標準函式庫」、「第三方套件」、「local app 套件」的順序寫，並且以一行空行將上述三塊區分開（若使用 VS Code 可以用 "isort" 這個 extension 自動排序）
3. 上述三塊中，內部最好以字母順序排序
4. 不要為了節省行數把不同 modules 擠在同一行 import

以下提供正確示範：

```Python
"""Illustration of good import statement styling.
Note that the imports come after the docstring.
"""

import datetime
import os

from flask import Flask
from flask_restful import Api

from local_module import local_class
from local_package import local_function
```

# 參考資料

<https://realpython.com/absolute-vs-relative-python-imports/>
