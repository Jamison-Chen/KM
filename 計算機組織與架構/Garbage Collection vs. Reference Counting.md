### Garbage Collection

#TODO

### Reference Counting

下面示範在 Python 中如何取得一個物件的 reference counting：

```Python
import sys

a = []
b = a
print(sys.getrefcount(a)) # 3
```

上例中，list object 被 reference 三次，分別是 `a`, `b` 以及傳入 `sys.getrefcount` 的參數。

#TODO
