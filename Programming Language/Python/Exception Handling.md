# 自行包裝 Exception

以下為各種寫法下的 error message：

### `raise A`

```Python
try:
    a = 1/0
except ZeroDivisionError:
    raise ValueError
```

Error message:

```plaintext
Traceback (most recent call last):
  File "/Users/bingyangchen/hello.py", line 2, in <module>
    a = 1 / 0
        ~~^~~
ZeroDivisionError: division by zero

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/bingyangchen/hello.py", line 4, in <module>
    raise ValueError
ValueError
```

請注意中間那句："During handling of the above exception, another exception occurred:"

### `raise A from B`

```Python
try:
    a = 1/0
except ZeroDivisionError as e:
    raise ValueError from e
```

Error message:

```plaintext
Traceback (most recent call last):
  File "/Users/bingyangchen/hello.py", line 2, in <module>
    a = 1 / 0
        ~~^~~
ZeroDivisionError: division by zero

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/bingyangchen/hello.py", line 4, in <module>
    raise ValueError from e
ValueError
```

此時中間那句變成："The above exception was the direct cause of the following exception:"

### `raise A from None`

```Python
try:
    a = 1/0
except ZeroDivisionError:
    raise ValueError from None
```

Error message:

```plaintext
Traceback (most recent call last):
  File "/Users/bingyangchen/hello.py", line 4, in <module>
    raise ValueError from None
ValueError
```

這種寫法下，沒有任何關於 `ZeroDivisionError` 的訊息在 error message 中，由此可見==這種寫法是不被推薦的==，因為這樣會很難 debug。
