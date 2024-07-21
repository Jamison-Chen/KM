Python 中 construct an instance 的語法為 `<CLASS_NAME>()`，比如 `Dog()`，這個動作背後可以細分為兩個步驟：

1. 創造一個空的 object
2. 初始化

這兩個步驟分別對應到 `__new__` 與 `__init__` 兩個 [magic methods](</Programming Language/Python/Magic Method & Magic Attribute.md>)，通常我們定義一個 class 時只會 override `__init__`，比較少 override `__new__`，有兩個原因：

- Python 中所有的 class 都預設繼承 `object` class，而 `object` 已經實作了 `__new__`
- 很少有其它事情非在 `__new__` 裡做不可

# 範例

下面這個例子或許可以幫助理解：

```Python
class Point:
    def __new__(cls, *args, **kwargs):
        print(args, kwargs)
        return super().__new__(cls)
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

p1 = Point(1, 2)  # (1, 2) {}

args = (1, 2)
p2 = Point.__new__(Point, *args).__init__(*args)  # (1, 2) {}
```

從上面這個例子可以注意到：

- `__new__` method 的第一個參數是 `cls`，不是 `self`，這代表這個 method 須要透過 class name 呼叫
- 從 code 看不到 `__new__` method 後面的參數（`*args` 與 `**kwargs`）被傳到其它地方（沒有被傳入 `super().__new__` 中）
- `__new__` 會 return 一個 instance，但 `__init__` 不會
- `Point(1, 2)` 的效果等同於 `Point.__new__(Point, 1, 2).__init__(1, 2)`

另外還有幾點值得注意的事：

- 上例中的 `super().__new__(cls)` 其實就是 `object.__new__(cls)`，因為 `Point` 沒有繼承其他 class 的話預設就是繼承 `object`
- `__init__` 只能 return `None`，且通常都是 implicitly return `None`
- 通常即使要 override `__new__`，method signature 也會是 `(cls, *args, **kwargs)`
- 建立 instance 時所需要的引數數量取決於 `__new__` 與 `__init__` 的 signature（只是通常 `__new__` 的 signature 是 `**args, **kwargs`，所以容易讓人誤以為引數數量只取決於 `__init__` 的 signature）

# 練習

現在讓我們來試試繼承 `float` 這個 built-in class，首先你可能會想這樣寫：

```Python
class Distance(float):
    def __init__(self, value, unit):
        super().__init__(value)
        self.unit = unit

in_miles = Distance(42.0, "mile")
```

執行後就會發現下面這樣的錯誤訊息：

```plaintext
in_miles = Distance(42.0, "mile")
           ^^^^^^^^^^^^^^^^^^^^^^
TypeError: float expected at most 1 argument, got 2
```

其實錯誤還不只如此，`super().__init__(value)` 這行也會有警告：Expected 0 positional arguments

會有這些錯誤的原因如下：

- Built-in class `float` 的值在 `__new__` method 裡就決定了，`float.__init__` 反而不接收任何參數（這是第二個錯誤訊息的原因）
- Built-in class `float` 的 `__new__` method 只接收一個參數（這是第一個錯誤訊息的原因）

要避開上述錯誤的方法即：

- 在 `Distance` 中 override `__new__` method，讓它接收兩個參數
- 在 `Distance` 的 `__new__` method 中傳遞 `value` 給 superclass（也就是`float`）的 `__new__` method

所以正確的寫法會是：

```Python
class Distance(float):
    def __new__(cls, value, unit):
        return super().__new__(value)
    def __init__(self, value, unit):
        super().__init__()
        self.unit = unit

in_miles = Distance(42.0, "mile")
print(in_miles, in_miles.unit)  # 42.0 mile
```

>[!Note]
>上面這個寫法中，我們將「通常即使要 override `__new__`，method signature 也會是 `(cls, *args, **kwargs)`」這個傳統打破了。

# 參考資料

- <https://realpython.com/python-class-constructor/>
