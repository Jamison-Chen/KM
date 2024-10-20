>[!Note]
>閱讀本文之前，你須要先認識 Python 中的 [Decorator](</Programming Language/Python/Decorator.md>)。

# The Built-In `@property` Decorator

### 取得「經過計算但性質類似一般 Property」的值

傳統上，當一個 class 有某些 proterties 是需要透過某些額外的運算才能得到值時，我們可能會寫一個 `get_xxx` function 來得到計算結果，像是下方例子中的 `get_full_name`：

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

就性質而言，full name 也算是一個 `Person` 天生的屬性，且永遠都等於 `f"{self.first_name} {self.last_name}"`，所以應該要像是 first name 與 last name 一樣可以直接用 `.full_name` 取得為佳，而這正是 `@property` decorator 可以達到的效果。

>[!Note]
>上面的這個例子可能不夠好，原因是 full name 的運算很簡單，其實可以在 `__init__` method 內直接定義 attribute `self.full_name = f"{self.first_name} {self.last_name}"` 就好了。
>
>但當須要更多行程式碼才能得到一個 "computed" property 時，就不適合將該邏輯寫在 `__init__` method 中了，此時 `@property` decorator 就能體現優勢。

### 讀取 Private Attribute 的值

有時候 class 的 private attribute 只是不想被隨意更動值，在外部還是希望可以讀取值，此時就可以使用 `@property` 來取值：

```Python
class Person:
    def __init__(self, first_name: str, last_name: str) -> None:
        self.__first_name = first_name
        self.__last_name = last_name

    @property
    def first_name(self) -> str:
        return self.__first_name

p = Person("John", "Doe")
print(p.first_name)  # John
```

通常被裝飾的 method 名稱會與 private attribute 同名但沒有 `__` prefix。

# Setter

使用 `@property` 裝飾的 methods 都是用來「取值」的 **getter method**，而若想透過 `instance.xxx = ...` 的方式設定 property 的值，則有以下寫法：

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

- Setter decorator 的命名必須為 `<GETTER_METHOD_NAME>.setter`
- Setter method 的命名雖然並不一定要與 getter method 相同，但通常會相同

Setter method 在當實際要被 assign value 的 attribute 為 private attribute 時常被使用。以上例而言，`__first_name` 與 `__last_name` 都是 private attributes，無法直接透過 `p.__first_name = "..."` 的方式設定新值，只能透過 `p.full_name = "..."` 來同時設定 first name 與 last name。

# Cached Property

之所以會用到 `@property` 來裝飾 method，而不直接在 `__init__` method 裡定義一個 attribute 並指派值給它，是因為這種 property 的值須要經過較複雜的運算才能得到，所以把這些「複雜的運算」寫成 method，再用 `@property` 裝飾之，使其可以用「形如」取一般 property 的方式來取得。

==每一次呼叫這些 `@property` 裝飾的 method 都會重新執行 getter method 內的運算（並不會把結果存起來）==，以先前 `Person` class 的例子而言，雖然呼叫 `p.full_name` 可以得到 `p` 的 full name，感覺好像 full name 就儲存在 `full_name` 這個變數內，但其實必非如此，每次呼叫其實都經過 getter method 把 first name 與 last name 串接後才得到 full name。

如果我們預期一個 getter method 所回傳的值不常變動，是不是可以不用每次都執行這個 getter method，而是可以直接取用先前運算的結果呢？確實有兩種方式可以達到這個目的：

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

在這個例子中，我們寫了一個 decorator `lazy_property`，`lazy_property` 會 return 一個 getter method (`_lazy_property`)，而這個 getter method 內使用到了 Python 內建的 `hasattr`、`getattr` 與 `setattr` 三個 functions，其邏輯為「如果在 instance 中找不到指定名稱的 attribute，就執行原始的 `func`，並把結果透過 `setattr` 存起來，以便下次直接取用」。

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

輸出值與法一相同。

這個例子使用的是自 Python 3.8 開始支援的 `functool.cached_property` decorator（是一個 [class](</Programming Language/Python/Decorator.md#Class as Decorator>)），這個 decorator 背後的原理本質上與法一相同，詳細可以參考 [source code](https://github.com/python/cpython/blob/7fc9be350af055538e70ece8d7de78414bad431e/Lib/functools.py#L965)，簡言之就是使用 `instance.__dict__.get(<ATTR_NAME>)` 與 `instance.__dict__[<ATTR_NAME>] = ...` 來取代法一的 `getattr(...)` 與 `setattr(...)`。

# 參考資料

- <https://www.geeksforgeeks.org/python-functools-cached_property/>
