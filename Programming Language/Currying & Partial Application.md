#FP

# Currying

>Currying 就是將「一個接收多個參數的 function」轉換成「一連串只接收 **一個** 參數的 functions 連續呼叫」。

假如現在要以 JavaScript 實作一個將兩數相加的 function，以 non-curried 的方法來寫，會長得像下面這樣：

```JavaScript
const f = (a, b) => a + b;

// Call the function
f(2, 3)  // 5
```

改寫成一個 curried function 後則會長得像這樣：

```JavaScript
const g = a => b => a + b;

// Call the function
g(2)(3)  // 5

// 也可以分兩步驟呼叫
let h = g(2)
h(3)  // 5
```

上面這個例子中，`g` 或者說 `a => b => a + b`，是一個 [[Higher-Order Function]]。

事實上，"currying" 這個動作也可以由一個 function 來執行，也就是說你也可以定義一個叫做 `curry` 的 function，用來把一個 non-curried function 變成 curryied function：

```JavaScript
const curry = f => a => b => f(a, b)

// A non-curried function
const f = (a, b) => a + b

// Currying the function
const g = curry(f)

// Call the curried function
g(2)(3)  // 5
```

# Partial Application

Partial Application 的概念源自於數學的「函數部分求值」，比如現在有一個函數 $f(x, y) = x^2 + y^2$，若想知道 x = 2 時的函數的樣子，當然就是將 x = 2 代入原函數。帶入後會得到 $f(2, y) = 2^2 + y^2 = y^2 + 4$，此時的 $f(2, y)$ 就是一個經過 partial application 的函數，我可以另外定義一個函數 $g$，並令 $g(y) = f(2, y)$。

上面的例子若以 JavaScript 表示就會變成：

```JavaScript
const f = (x, y) => x**2 + y**2

// Partial Application
const g = y => f(2, y)

g(3)  // 13
```

### Partial Application 與 Currying 相關，但不完全相同

以下分別示範將一個接收多個參數的 function `f` 進行 currying 以及 partial application 的過程：

```JavaScript
// A function that takes three arguments
const f = (a, b, c) => a**2 + b**2 + c


// Currying
// Step1: Define a function that curries another function taking three args
const curry = f => a => b => c => f(a, b, c)

// Step2: Curry the function `f`
const g = curry(f)

// Step3: Apply the first argument to `g` to derive another function
const h = g(2)

// Step4: Apply the second argument to `h` to derive another function
const i = h(3)

// Step5: Apply the third argument to `i` to derive the final value
console.log(i(4))  // 17


// Partial Application
// Step1: Apply `f` with the first argument to derive another function
const j = (a, b) => f(2, a, b)

// Step2: Call the derived function `j`
console.log(j(3, 4))  // 17
```

一個 curried function 的 **arity** (接收參數的數量) 必為 1；經過 partial application 後所得到的 function 的 arity 則有可能大於 1，這個現象會在原函數接收的參數超過兩個時開始體現出來。

至此為止，前面所有範例都是給定第一個參數值，當然也可以給定其他位置的參數的值，只是此時 currying 與 partial application 的做法也會不同：

```JavaScript
const f = (a, b, c) => a + b * c

// Currying (assuming that we already have a `curry` function)
const g = curry(f)

const h = a => c => g(a)(3)(c)

console.log(h(2)(4))  // 14


// Partial Application
const i = (a, c) => f(a, 3, c)

console.log(i(2, 4))  // 14
```

你會發現，在 currying 的過程中，為了保持 `h` 的 arity 為 1，因此定義 `h` 時必須額外做一次 currying。

# 原理

Currying 與 Partial Application 皆利用了 [[Closure]] 的特性，將 HOF 中具有值的變數或參數交給自己 return 的 child function，使得這些變數或參數在 child function 中仍保有意義與值。

# 優點

將一個複雜的 function 拆分成若干個基本 functions 的組合，可以提高這些基本 function 的重複使用性。

# 實作 `curry` Function

理想上我們希望存在一個 `curry` function 可以將 arity 為 n 的 non-curried function 轉換為 arity 為 1，且可以連續呼叫 n 次的 curried function chain。實作這樣的 function 須要使用到 recursion 的概念：

```JavaScript
function curry(func, original_func_args_len = func.length, call_time = 1) {
    if (original_func_args_len === call_time) return func;

    return (arg) =>
        curry(
            (...args) => func(arg, ...args),
            original_func_args_len,
            call_time + 1
        );
}
```

# 參考資料

- <https://en.wikipedia.org/wiki/Currying>
- <https://en.wikipedia.org/wiki/Partial_application>
- <https://mostly-adequate.gitbook.io/mostly-adequate-guide/ch04>
