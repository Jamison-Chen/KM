>[!Note]
>閱讀本文之前，你須要先認識 Python 中的 [[Decorator]]。

# The Built-In `@property` Decorator

在 Python 中，當一個 class 有某些 proterty 是需要透過某些額外的運算才能得到值時，我們可能會這樣寫：

```Python
class Person:
    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

p = Person("John", "Doe")
print(p.get_full_name())  # John Doe
```

但比較好的寫法使用 Python 內建的 `@property` decorator：

```Python
class Person:
    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

p = Person("John", "Doe")
print(p.full_name)  # John Doe
```

為什麼說比較好呢？對照上方兩個例子後我們可以發現，當使用傳統的 method 時，要取得 `full_name` 時就必須用傳統 call method 的方式（method name 後面要加 `()`）但就性質而言，full name 應該要像是 first name 與 last name 一樣可以直接用 `.full_name` 取得為佳，而這正是 `@property` decorator 可以達到的效果。

>[!Note]
>上面的這個例子可能不夠好，原因是 full name 的運算很簡單，其實可以在 `__init__` method 內直接定義 attribute `self.full_name = f"{self.first_name} {self.last_name}"` 就好了。
>
>但當須要更多行程式碼才能得到一個 "computed" attribute 時，就不適合將該邏輯寫在 `__init__` method 中，此時就能體現使用 `@property` decorator 的優勢了。

### Setter

上面「取得」full name 的 property-decorated method 屬於一種 **getter method**，有時候除了取值以外，我們還會想設定值，針對 property-decorated method，可以有以下寫法：

```Python
class Person:
    def __init__(self, first_name: str, last_name: str) -> None:
        self.__first_name = first_name
        self.__last_name = last_name

    @property
    def full_name(self) -> str:
        return f"{self.__first_name} {self.__last_name}"

    @full_name.setter
    def full_name(self, full_name: str) -> None:
        self.__first_name, self.__last_name = full_name.split(" ")

p = Person("John", "Doe")
p.full_name = "Harry Potter"
print(p.full_name)  # Harry Potter
```

- Setter decorator 的命名必須為 `<GETTER_METHOD_NAME>.setter`。
- Setter method 的命名雖然並不一定要與 getter method 相同，但通常會相同。

Setter method 在當實際要被 assign value 的 attribute 為 private attribute 時常被使用。以上例而言，`__first_name` 與 `__last_name` 都是 private attributes，無法直接透過 `p.__first_name = "..."` 的方式設定新值，只能透過 `p.full_name = "..."` 來同時設定 first name 與 last name。

# Cached Property

之所以會用到 `@property` 來裝飾 method，而不直接在 `__init__` method 裡定義一個 attribute 並指派值給它，是因為這種 property 的值須要經過較複雜的運算才能得到，所以把這些「複雜的運算」寫成 method，再用 `@property` 裝飾之，使其變成 getter method，在外部可以用「形如」取一般 attribute 的方式來取得。

然而其實每一次呼叫這些裝飾過的 property 時，都會執行 getter method 內的運算（並不會把結果存起來）。以先前 `Person` class 的例子而言，雖然呼叫 `p.full_name` 可以得到 `p` 的 full name，感覺好像 full name 就儲存在 `full_name` 這個變數內，但其實必非如此，每次呼叫其實都經過 getter method 把 first name 與 last name 串接後才得到 full name。

不過如果我們預期一個 getter method 所回傳的值不常變動，是不是可以不用每次都執行這個 getter method，而是可以直接取用先前運算的結果呢？

確實有兩種方式可以達到這個目的：

### 法一：`setattr` & `getattr`

讓我們看看下面這個例子：

```Python
def lazy_property(func):
    attr_name = f"_{func.__name__}"

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    return _lazy_property


class Person:
    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

    @lazy_property
    def full_name(self) -> str:
        print("Do some expensive calculation...")
        return f"{self.first_name} {self.last_name}"


p = Person("John", "Doe")

print(p.full_name)
# Do some expensive calculation...
# John Doe

print(p.full_name)  # John Doe
```

可以發現 "Do some expensive calculation..." 只有在第一次呼叫 `.full_name` 時才被印出來，代表第二次呼叫時並沒有執行 getter method。

在這個例子中，我們寫了一個 decorator `lazy_property`，`lazy_property` 會 return 一個 getter method `_lazy_property`，而這個 getter method 內使用到了 Python 內建的 `hasattr`、`getattr` 與 `setattr` functions，其邏輯為「如果在 instance 中找不到指定名稱的 attribute，就執行原始的 `func`，並把結果透過 `setattr` 存起來，以便下次直接取用」。

### 法二：`functools.cached_property`

>[!Note]
>這個方法只適用於 Python 3.8 之後的版本。

一樣先看範例：

```Python
from functools import cached_property

class Person:
    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

    @cached_property
    def full_name(self) -> str:
        print("Do some expensive calculation...")
        return f"{self.first_name} {self.last_name}"

p = Person("John", "Doe")

print(p.full_name)
# Do some expensive calculation...
# John Doe

print(p.full_name)  # John Doe
```

結果與法一相同。

這個例子使用的是自 Python 3.8 開始支援的 `functool.cached_property` decorator（是一個 class），這個 decorator 背後的原理本質上與法一相同，詳細可以參考 [source code](https://github.com/python/cpython/blob/7fc9be350af055538e70ece8d7de78414bad431e/Lib/functools.py#L965)，簡言之就是使用 `instance.__dict__.get(<ATTR_NAME>)` 與 `instance.__dict__[<ATTR_NAME>] = ...` 來取代法一的 `getattr` 與 `setattr` function。
