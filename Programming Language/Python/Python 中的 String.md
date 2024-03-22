### Immutable String Object

Python 中的 string 物件是 immutable 的，關於 immutable string 的詳情，請見[[Mutable String & Immutable String|本文]]。

### f-string

- f-string 指的是在 string quotes 前方有 prefix `f` 或 `F` 的 string
- 用途：string formatting
- Python 3.6 之後才可使用
- 取代原本的 `<STRING>.format(...)`
- [官方文件](https://docs.python.org/3/reference/lexical_analysis.html#formatted-string-literals)

e.g.

```Python
name = "Bob"

# Before Python 3
print("My name is %s." % name)  # My name is Bob.

# After Python 3, before Python 3.6
print("My name is {name}.".format(name=name))  # My name is Bob.

# After Python 3.6
print(f"My name is {name}.")  # My name is Bob.
```

---

在 f-string 中若必須使用 quotation，則須 `"` 與 `'` 交錯使用：

```Python
data = {"name": "Bob"}
print(f"My name is {data['name']}."  # My name is Bob.
```

---

由於 f-string 使用 `{}` 來挖空格，所以若要印出 `{` 則須寫 `{{`，要印出 `}` 則須寫 `}}`：

```Python
name = "Bob"
print(f"{{My {{name}} is {name}.")  # {My {name} is Bob.
```

---

在 debug 時，常常會需要同時印出變數的名稱與變數的值，Python 3.8 後，你可以在 `{}`
中使用 `=`：

```Python
line = "The mill's closed."

# Before Python 3.8
print(f"line = {line}")  # line = The mill's closed.

# After Python 3.8
print(f"{line = }")  # line = The mill's closed.
```

---

一般而言，變數在 f-string 中對會被呼叫 `__str__` method 來取得 string，但若在 `{}` 中使用 `!r` 就會改成呼叫變數的 `__repr__`：

```Python
line = "I'm beautiful."
print(f"He said {line}")  # He said I'm beautiful.
print(f"He said {line!r}")  # He said "I'm beautiful."
```

關於 `__str__` 與 `__repr__` 的差別，請見[[__repr__ 與 __str__|本文]]。

---

在 `{}` 中也可以使用 `:` 進行特殊的 formatting：

```Python
from datetime import datetime

today = datetime(year=2023, month=1, day=1)
print(f"{today:%B %d, %Y}")  # January 01, 2023
```
### r-string

- r-string 指的是在 string quotes 前方有 `r` 的 string
- r-sting 中的內容會被視為 [regular expression](https://regex101.com/)

### b-string

- b-string 的型別是 byte 不是 string
- b-string 中只能有 ASCII characters

```Python
print(b"abc" == "abc")  # False

print(b"你好")
# SyntaxError: bytes can only contain ASCII literal characters
```

### String Literal Concatenation

`"hello" "world"` 等價於 `"helloworld"`，但串接的過程是在 compile time 完成的，而變數的值是在 run time 才決定的，所以不可以直接拿兩個 string 變數這樣做，兩個變數串接還是須要使用 `+` operator。

```Python
print("abc" "def")  # abcdef

a = "abc"
b = "def"
print(a b)
# SyntaxError
```

# 參考資料

- <https://docs.python.org/3/reference/lexical_analysis.html#literals>
- <https://docs.python.org/3/library/string.html>
