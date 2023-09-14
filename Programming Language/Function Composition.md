#FP

>[!Note]
>Function composition 與 OOP 中的 [[Object Composition]] 是不同的東西。

Function composition 的概念源自於數學，泛指「將兩個函式 $g$、$f$ 組合成另一個函式 $h$（表示成 $h=g \circ f$）進而使得 $h(x)=g(f(x))$」的動作。

負責組合函式的函式叫做 composition function，而通常 composition 的產物會被叫做 **pipeline**。

實務上定義 composition function 時，不會只接受兩個 functions 作為參數，而是會不限制參數個數，然後「由內而外」一步步將上一層函式的 ouput 當作下一層函式的 input，實際做法如下：

```JavaScript
function compose(...funcs) {
    return (x) => {
        let output = x;
        for (const f of funcs) output = f(output);
        return output
    }
}
```

恰巧，JavaScript 中的 `Array` prototype 有 `reduce` method，可以讓程式碼更佳簡潔：

```JavaScript
function compose(...funcs) {
    return (x) => funcs.reduce((v, f) => f(v), x);
}
```

無論是上述哪個例子，都可以看見 composition function 不但接收 function 作為參數，也回傳 function，由此可見 composition function 屬於 [[Higher-Order Function (HOF)]]。

使用 `compose` function 的例子如下：

```JavaScript
const double = (x) => x * 2;
const sqrt = (x) => Math.sqrt(x);
const f = compose(double, sqrt);

console.log(f(50))  // 10
```

可以注意到，由於前面我們定義的 `compose` function 的 output 是一個 **arity** (接收參數的數量) 為 1 的 function (unary function)，因此所有放入 `compose` 的也都必須是 unary functions。

# 函式呼叫順序

請注意被 composed 的函式們被呼叫的順序，以上面的程式碼而言，順序是由左往右的，不過其實嚴格來說，這個順序和本文開頭寫的數學定義是相反的，若要求完全符合數學上的定義，應將 composition function 改寫為：

```JavaScript
function compose(...funcs) {
    return (x) => funcs.reverse().reduce((v, f)=>f(v), x)
}
```

# Why Composition?

[[Currying & Partial Application]] 的目標是把複雜的 function 拆解成數個小 functions，以增加這些小 functions 的 reusability，composition 的角色則是利用這些小 functions 組合成各種其他複雜 functions。

# 參考資料

- <https://ithelp.ithome.com.tw/articles/10237503>
- <https://en.wikipedia.org/wiki/Function_composition_(computer_science)>
