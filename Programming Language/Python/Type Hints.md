Python 作為一個 [動態型別](</Programming Language/程式語言的分類.md#動態型別>) 的語言，雖然享受著「開發速度快」及「容易上手」等美名，不過隨著專案越來越龐大，開發和 debug 的速度卻會因缺乏型別定義而下降，出現 bug 的機率也隨之上升。

不過 Python 自 3.5 推出後便導入 Type Hint 機制，開始擁抱靜態型別的優點，舉例如下：

```Python
def greet(name: str) -> None:
    print(f"Hello, my name is {name}.")

n: str = "Chris"
greet(n)
```

由上面的例子我們可以發現：

- 定義 variables 以及 parameters 時使用 `: {TYPE}`
- 定義 functions 時使用 `-> {TYPE}`。
- 當 `None` 用作 function 的 return type 時，意思是「沒有 `reurtn` statement，或 explicitly `return None`，或 simply `return`」

須注意的是，Python 的 Type Hints 是一種輔助用的功能，是給 developer 和 editor 看的，不是給 Python Interpreter 看的，沒有 runtime checker，也不影響 Python 身為動態型別的本質。

換句話說，如果你用了 Type Hints，然後在程式碼裡面把一個 `int` assign 給型別為 `str` 的變數，還是可以執行（你只會在 editor 上看到五顏六色的底線）。

# 常用的 Types

### Primitive Types

常用的 primitive types 包括：`int`, `float`, `str`, `None`。

### Non-Primitive Types

常用的 non-primitive types 包括：`Tuple`, `List`, `Set` 與 `Dict`。

- `List[X]`：一個全部元素都是 `X` 型別的 list，比如 `List[int]`
- `Tuple[X]`：一個全部元素都是 `X` 型別的 tuple，比如 `Tuple[int]`
- `Tuple[X, ...]`：一個「第一個元素是 `X` 型別」，「其餘元素可以是任何型別」的 tuple，比如 `Tuple[int, ...]`

    `...` 在這裡的意思不是懶得寫，而是叫 ellipsis 的語法。

- `Set[X]`：一個全部元素都是 `X` 型別的 set，比如 `Set[int]`
- `Dict[X, Y]` ：一個全部的 key 型別都是 `X`，且全部的 value 型別都是 `Y` 的 dict

>[!Info]
>上述的 non-primitive types 皆必須先 `from typing import {TYPE}` 才能使用，但在 Python 3.9 之後有 built-in types 可以取代之（就不用 import 了），詳見 [此段](</./Programming Language/Python/Type Hints.md#After Python 3.9>)。

### Special Types

##### `Union[X, Y]`

型別可以是 `X` 或 `Y`，比如 `Union[int, float, None]`。

須先 `from typing import Union`，但在 Python 3.10 後可以用 `X | Y` 取代之。

##### `Optional[X]`

型別可以是 `X` 或 `None`，比如 `Optional[int]`。

須先 `from typing import Optional`，但在 Python 3.10 後可以用 `X | None` 取代之。

##### `Callable[[Arg1Type, Arg2Type], ReturnType]`

若一個 function 的接收兩個型別分別為 `Arg1Type` 與 `Arg2Type` 的參數，且 return 的型別為 `ReturnType` 的值，則該 function 的型別可以定義如上。

若想要定義一個「不限制參數的數量與型別」的 function，則可以寫：`Callable[..., ReturnType]`。

##### `ClassVar[T]`

定義 class variable 時可以使用它，`T` 的部分就是原本的資料型態，比如 `ClassVar[int]`。

# After Python 3.8

### `Literal`

規範某變數或 function 的回傳值只能為某些特定值，舉例如下：

```Python
from typing import Literal

def open_helper(file: str, mode: Literal["r", "rb", "w", "wb"]) -> str:
    ...
```

### `Final`

定義某變數為常數，效果類似 JavaScript 中的 `const`，舉例如下：

```Python
from typing import Final

PI: Final[float] = 3.14159

PI = 0  # Error reported by type checker
```

>[!Note] 注意
>現在還無法檢查到 `+=` 等 Augmented Assignment，以上例而言，`PI += 1` 是不會出現錯誤提示的。

# After Python 3.9

在 Python 3.9 前，`Tuple`, `List`, `Set`, `Dict` 等 types 要從 `typing` module import，不過 3.9 後可以直接使用 built-in 的 `tuple`, `list`, `set` 與 `dict` 替代之，`Tuple`, `List`, `Dict` 等則變為 deprecated，詳情請見 [官方文件](https://docs.python.org/3/library/typing.html#corresponding-to-built-in-types)。

Before 3.9:

```Python
from typing import Tuple, List, Dict

a: Tuple[int] = (0, )
b: List[str] = ["a"]
c: Dict[str, int] = {"a": 0}
```

Since 3.9:

```Python
a: tuple[int] = (0, )
b: list[str] = ["a"]
c: dict[str, int] = {"a": 0}
```

# After Python 3.10

### `X | Y` 取代 `Union[X, Y]`

### `X | None` 取代 `Optional[X]`

### `TypeAlias`

可以把型別存成變數，舉例如下：

```Python
from typing import TypeAlias

MODE: TypeAlias = Literal["r", "rb", "w", "wb"]
def open_helper(file: str, mode: MODE) -> str:
    ...
```

# After Python 3.12

### The `type` Statement

定義一個名為 `Point` 的 type alias：

```Python
type Point = tuple[float, float]
```

也可以使用 generic：

```Python
type Point[T] = tuple[T, T]
```

### The `@override` Decorator

```Python
from typing import override

class Parent:
    def foo(self) -> int:
        return 1

    def bar(self, x: str) -> str:
        return x

class Child(Parent):
    @override
    def foo(self) -> int:
        return 2

    @override
    def bar(self) -> int:  # Type check error: no matching signature in ancestor
        return 1
```

# 參考資料

- [官方文件](https://docs.python.org/3/library/typing.html)
- [PEP 484](https://peps.python.org/pep-0484/)
