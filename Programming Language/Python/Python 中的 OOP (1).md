#OOP

Python 是一種 multiparadigm 的程式語言，OOP 是其中一種 Python 支援的 paradigm。

# Encapsulation

### "類" Private Attribute/Method

e.g.

```Python
class Human:
    def __init__(self):
        self.__max_age = 100

h = Human()
print(h.__max_age)

# Traceback (most recent call last):
# ...
#     print(h.__max_age)
#           ^^^^^^^^^^^
# AttributeError: 'Human' object has no attribute '__max_age'
```

由上方的 error message 可知上例中的 `__max_age` 無法從 class 外部透過 `物件.__max_age` 的方式存取，只能在 class 內以 `self.__max_age` 的方式來存取，這是 Python 為了符合 OOP 中 [[OOP 四本柱#封裝 (Encapsulation)|Encapsulation]] 這個性質所採取的做法。

為什麼說是 "類" private 呢？這是因為==其實有方法可以在 class 外取得以雙底線開頭的 attribute 與 method==，承接上面 `Human` 的例子：

```Python
h = Human()
print(h._Human__max_age)  # 100
```

>其實 Python 中並沒有真正的 encapsulation。

### Name Mangling

Name mangling 的白話文就是「改個名字」，Python interpreter 會在 compile time 將以雙底線 (`__`) 開頭的 attribute/method name 的前面加上 class name 作為 prefix，藉此達到「無法在 class 外直接存取以雙底線 (`__`) 開頭的 attribute/method 」的效果，但只要我們知道這個改名字的規則，就可以存取它們了，就像上面例子中的 `h._Human__max_age`。

>[!Info]
>其實 name mangling 的初衷只是為了在繼承時不要出現 naming conflicts。

### 沒有 `protect`

Python 中完全沒有其它 OOP 語言中 **protect** 這個概念，社群上只有「用 `_` 作為 attribute/method name 的開頭」這種傳統／建議／風格。

# Inheritance

### `object`

Python 中所有 class 即使沒有特別聲明要繼承誰，預設都會繼承 `object` class。

### Multiple Inheritance

Python 中的 class 可以進行 multiple inheritance：

```Python
class S1:
    ...

class S2:
    ...

class T(S1, S2):  # multiple inheritance
    ...
```

但也因為 multiple inheritance，所以可能出現 [[OOP 零碎筆記#Diamond Problem|diamond problem]]（不知道調用 superclasses 的 method 時的優先順序），Python 的解決方法是使用 [C3 linearization](https://en.wikipedia.org/wiki/C3_linearization) 演算法取得 method resolution order (MRO)（可以使用 `<CLASS>.__mro__` 查看）。

### `super`

使用 `super().<METHOD>` 可以在 subclass 呼叫 superclass 的 method，常用於 method overriding 或 overloading 時，如果「method 在 subclass 要做的事情是 method 在 superclass 要做的事情再加上其它事情」，則「method 在 superclass 要做的事情」可以使用 `super().<METHOD>` 來達到 code reuse：

```Python
class S:
    def __init__(self, a):
        self.a = a
    def method_1(self):
        print("hello")

class T(S):
    def __init__(self, a, b):
        super().__init__(a)
        self.b = b
    def method_1(self):
        print("hi")
```

`super` 會處理好 multiple inheritance 引發的「superclass mehtod 調用優先順序」的問題，它會根據 MRO 的順序決定要用哪個 superclass 的 method。

>[!Note]
>若 subclass 中有定義自己的 `__init__` method，則一定要在 method 的第一行先呼叫 superclass 的 `__init__` method。

# Abstract Class

==Python 中並沒有 interface 的概念，取而代之的是 **abstract class**==（關於 interface 與 abstract class 的差別請見[[OOP 四本柱#Interface vs. Abstract Class|本文]]），"interface" 在 Python 中也不是保留字／關鍵字。

要建立一個 abstract class 的關鍵步驟有三：

- `import abc`
- Abstract class 繼承 `abc.ABC` class，或令 `metaclass=abc.ABCMeta`
- 使用 `@abc.abstractmethod` 裝飾 abstract class 中的 abstract method

e.g.

```Python
from abc import ABC, abstractmethod

class MyAbstractClass(ABC):
    @abstractmethod
    def method1(self):
        raise NotImplementedError

# or

class MyAbstractClass(metaclass=ABCMeta):
    @abstractmethod
    def method1(self):
        raise NotImplementedError
```

接著就是繼承 abstract class 並實作：

```Python
class MyClass(MyAbstractClass):
    def method1(self):
        print("Implementation of method1")
```

若沒有完整實作，則會在初始化物件時出現 TypeError：

```Python
class MyIncompleteClass(MyAbstractClass):
    def another_method(self):
        print("hello world")

test = MyIncompleteClass()  # TypeError: Can't instantiate abstract class MyIncompleteClass with abstract method method1
```

Abstract class 中也可以有 concrete method，比如下例中的 `method2`：

```Python
from abc import ABC, abstractmethod

class MyAbstractClass(ABC):
    @abstractmethod
    def method1(self):
        raise NotImplementedError

    def method2(self):
        return 1 + self.method1()
```
