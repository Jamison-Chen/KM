# Closure & Captured Variable

#TODO

# 避免使用 Mutable Object 當作參數的預設值


Python 中的 function parameters 有以下幾個重要觀念：

- 所有 function parameters 的預設值都會「在 run time 前」就被計算出來
- 若 parameter 的預設值為 mutable，則該預設值就只會被分配到一塊記憶體空間，無論 function 被執行幾次

從第一點可知，最好不要將 parameter 的預設值設為另一個 function 運算後的結果，因為這容易造成誤解，不熟悉的人可能會以為每次 call function 時都會重新計算一次預設值。

```Python
from datetime import datetime
from time import sleep

# 錯誤示範
def f(d: datetime.now()):
    return d

if __name__ == "__main__":
    before = f()
    sleep(1)
    after = f()
    assert before < after

# AssertionError
```

從第二點可知，無論 function 被呼叫多少次，每一次呼叫時若要拿預設值，都會去固定的 memory address 讀取資料，所以若先前的 function calls 有改到值，後續的 function calls 就會拿到被改動後的結果。

```Python
# 錯誤示範
def f(l=[]):
    print("before:", l)
    l.append(1)
    print("after:", l)

if __name__ == "__main__":
    f()
    f()

# before: []
# after: [1]
# before: [1]
# after: [1, 1]
```

>[!Note]
>並不是所有程式語言都像 Python 一樣有上述兩點特性，比如在 Node.js 中，function parameters 的預設值是在 run time 算出來的，且每次 function call 的 parameter 的預設值都有獨立的記憶體空間。 
