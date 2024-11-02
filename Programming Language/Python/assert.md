### Statement Pattern

```plaintext
assert {EXPRESSION>[, {MESSAGE}]
```

其中 `{EXPRESSION}` 必須輸出一個 `bool`，`{MESSAGE}` 則必須是一個 `str`。

若 `{EXPRESSION}` 爲 `True`，則程式就會正常地繼續執行；反之，若 `{EXPRESSION}` 爲 `False`，則程式會中斷並出現錯誤訊息：

```plaintext
Traceback (most recent call last):
  File ..., line ...
    assert {EXPRESSION}, {MESSAGE}
           ^^^^^^^^^^^^
AssertionError: {MESSAGE}
```

### 如何忽略 `assert`？

執行一個 Python module 時，若加上 `-0` option，則 Python Interpreter 會略過所有 `assert` statement。

e.g.

```bash
python my_module.py -0
```

加上 `-0` option 實際上是把該 module 的 `__debug__` 這個 [magic attributes](</Programming Language/Python/Magic Method & Magic Attribute.md>) 設為 `False`，因此，我們可以說：

```Python
assert {EXPRESSION}, {MESSAGE}

# is equivalent to

if __debug__:
    if not {EXPRESSION}:
        raise AssertionError({MESSAGE})
```
