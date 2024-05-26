我們都知道，在一個 function 內定義的變數或參數，在該 function 外是不具意義的，以 Python 舉例如下：

```Python
def f(x):
    y = 0
    print(x, y)

print(f(0))  # 0 0
print(x, y)  # NameError: name 'x' is not defined
```

這樣看起來，一個變數的生命週期似乎是「始於其被定義時，終於離開當前的 function／function return 時」。

但是！其實上面這句話只在沒有 closure 來攪和的情況下才正確，==closure 就像一個保護膜，可以讓變數在脫離當前的 function 後仍然存活==。

那要怎麼製造 closure 呢？其實很簡單：

>在一個 (outer) function 內定義一個 inner function，並將 inner function 做為 outer function 的 return value，或者將 inner function 傳給 outer function 內的其他 function。

用 Python 寫就會長得像這樣：

```Python
def f(x):
    def g(y):
        return x + y
    return g

a = f(1)
print(a(2))  # 3
```

# Captured Variables

觀察上面的例子你可以發現，在執行完 `a = f(1)` 後，本來輸入 `f` 的引數 1 應該不再具有意義的，但這次卻被 function `g` 保護了起來，使得 `x` 在 `g` 中仍然具有意義，其值為 1。

同樣的道理，在 `f` 中可以存取的所有變數其實都可以放入 `g`，使得即使 `f` 執行完畢，`g` 也仍然記得那些變數的值，而這些被記住的變數們就叫做 **Captured Variables**。

### JavaScript 中無法被 Captured 的 Variables

在 JavaScript 中，以下兩個變數不會被 captured：

1. `this`
2. `arguments`

也就是說，inner function 中的 `this` 指的並不會是 outer function，而是 inner function 自己（除非 inner function 是一個 arrow function）；inner function 中的 `arguments` 指的也不是 outer function 的 arguments，而是 inner function 自己的 arguments。

# Function Scope

一個 function 的 function scope 可以被簡單理解為：「哪些地方的 variables 與 functions 對這個 function 而言有意義／可被存取？」

一個 function 的 scopt (作用域) 至少包含以下兩個：

1.  自己內部
2. 全域

另外，如果一個 function 是另一個 function 的 inner function，則 outer function 是它的第三個作用域，這個概念可以從最內部的 function 一直往外層延伸，形成所謂的 **scope chain**。也因為每次運用 closure 的特性來存取 outer function scope 的變數時，都會尋遍整個 scope chain（找不到就往上一層 function 找），因此其實這是一個 expensive 的語法。

# Closure 間不會互相干擾

首先看一下範例程式碼：

```Python
def f():
    l = [0]
    def g():
        return l
    return g

a = f()
b = f()
a()[0] = 1
print(b())  # [0]
```

在 Python 裡，變數是用 reference 的方式來存取 list，所以若兩個變數 refer 同一個記憶體位置，則當其中一方對該 list 做更動時，另一方所讀取到的值也會跟著連動；反之，若兩個變數 refer 不同的記憶體位置，那麼這兩個變數彼此間就是獨立的。

而由上面的例子我們可以看到，在 `a()` 將 list 從 `[0]` 改為 `[1]` 後，`b()` 所存取到的 list 並沒有跟著變，由此可知，不同的 closure 間的環境是相互獨立的，這使得「透過呼叫 function `f` 得到 function `g`」所達到的效果類似於「將 class 實例化為 instance」，事實上這也是 [[Factory Function vs. Constructor|factory function]] 背後的精髓。

>[!Note]
>Global variables 在不同 closures 間是共享（會連動）的，因為所有的 closures 都是 refer 同一個記憶體位置來存取 global variables：
>
>```Python
>l = [0]
>
>def f():
>    def g():
>        return l
>    return g
>
>a = f()
>b = f()
>a()[0] = 1
>print(b())  # [1]
>```

# Python 中的 Captured Variables

下面這段 JavaScript 程式碼是可以正常運行的：

```JavaScript
function f(x) {
    let arr = [1, x];
    
    function g() {
        arr = [arr[1], arr[0]];
        return arr;
    }
    
    return g;
}

let h = f(0);
console.log(h())  // [0, 1]
```

然而類似的概念在 Python 中卻會出錯：

```Python
def f(x):
    arr = [1, x]

    def g():
        arr = [arr[1], arr[0]]
        return arr

    return g

h = f(0)
print(h())
# UnboundLocalError: local variable 'arr' referenced before assignment
```

Why? 這是因為在任何 function 裡，當一個變數「首次出現」且準備被 assign value（即出現在 `=` 左側）時，Python interpreter 就會自動將該變數視為一個全新的 local variable。

所以上方例子中，當在 function `g` 裡執行到 `arr =` 時，`arr` 就已經不是從 `f` 抓來的 captured variable 了。

一個全新的 variable 必須先被 assign value 才能被 refer，所以 function `g` 裡的 `[arr[1], arr[0]]` 的 `arr` 此時是一個不具意義的 local variable，所以才會出現 `local variable 'arr' referenced before assignment` 這個錯誤。

### `nonlocal`

那要如何解決這個問題呢？在 Python 中有一個關鍵字叫做 `nonlocal`，它就是專門用來解決這類問題的，具體的使用方法如下：

```Python
def f(x):
    arr = [1, x]

    def g():
        nonlocal arr
        arr = [arr[1], arr[0]]
        return arr

    return g

h = f(0)
print(h())
```

其實就是在 inner function 的開頭先宣告「`arr` 不是 local variable」。須注意的是，「不是 local variable」並不意味著「是 global variable」，因此不能使用 `global` 關鍵字。

# Closure 的應用場景

1. 使用 [[Factory Function vs. Constructor#Factory Function|factory function]] 建立 object
2. [Currying](</Programming Language/Currying & Partial Application.md#Currying>)
3. [Partial Application](</Programming Language/Currying & Partial Application.md#Partial Application>)

# 參考資料

- <https://medium.com/javascript-scene/b2f0d2152b36>
