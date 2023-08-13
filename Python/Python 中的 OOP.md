#OOP

# Python 中的 Encapsulation

### "類" Private attribute/method

e.g.

```Python
class Human:
    def __init__(self):
        self.__max_age = 100

h = Human()
print(h.__max_age)  # AttributeError: 'Human' object has no attribute '__max_age'
```

由上方的 error message 可知上例中的 `__max_age` 無法從 class 外部透過 `物件.__max_age` 的方式存取（只能在 class 內以 `self.__max_age` 的方式來存取），這是 Python 為了符合 OOP 中 [[OOP 四本柱#封裝 (Encapsulation)|Encapsulation]] 這個性質所採取的做法。

為什麼說是 "類" private 呢？這是因為==其實有方法可以在 class 外取得以雙底線開頭的 attribute 與 method==，承接上面 `Human` 的例子：

```Python
h = Human()
print(h._Human__max_age)  # 100
```

>其實，Python 中並沒有真正的 encapsulation。

首先，Python 中完全沒有其它 OOP 語言中 **protect** 這個概念（社群上只有「用 `_` 作為 attribute/method 開頭」這種傳統／建議／風格）。

至於 **private** 呢，如同我們前面所見，是有方法可以繞過去的。這是因為其實 Python 是透過 **"Name Mangling"**（白話文就是「改個名字」）來達到「無法在 class 外直接 access 以 `__` 開頭的 attribute/method 」的效果，但只要我們知道名字被改成什麼，就可以 access 了。

>其實 Name Mangling 的初衷只是為了在 inheriting 時不要出現 naming conflicts。

# Python 中的 Inheritence

#TODO 

# Python 中的 Interface

其實嚴格來說，Python 中並沒有 interface 的概念，取而代之的是 **Abstract Class**（關於 interface 與 abstract class 的差別請見[[OOP 四本柱#Interface vs. Abstract Class|本文]]），在 Python 中 `interface` 也不是保留字／關鍵字。

要建立一個 abstract class 的關鍵步驟有二：

1. 繼承 `abc.ABC` class，或令 `metaclass=abc.ABCMeta`
2. 使用 `@abc.abstractmethod` 裝飾 method

e.g.

```Python
from abc import ABC, abstractmethod

class MyInterface(ABC):
    @abstractmethod
    def method1(self):
        raise NotImplementedError

    @abstractmethod
    def method2(self, arg1, arg2):
        raise NotImplementedError

# or

class MyInterface(metaclass=ABCMeta):
    @abstractmethod
    def method1(self):
        raise NotImplementedError

    @abstractmethod
    def method2(self, arg1, arg2):
        raise NotImplementedError
```

接著就是繼承 abstract class 並實作：

```Python
class MyClass(MyInterface):
    def method1(self):
        print("Implementation of method1")

    def method2(self):
        print("Implementation of method2")
```

若沒有完整實作，則會在初始化物件時出現 TypeError：

```Python
class MyIncompleteClass(MyInterface):
    def method1(self):
        print("Implementation of method1")

test = MyIncompleteClass()  # TypeError: Can't instantiate abstract class MyIncompleteClass with abstract method method2
```
