#FP  

# 定義

符合下列任一條件的 function，就是 HOF：

- 接收一個以上的 function 作為參數（通常做為引數的這些 function 會被稱為 **procedural parameter**）
- Return 一個 function

不是 HOF 者，則稱為 first-order function。

# 舉例

以 JavaScript 為例：

```JavaScript
const doTwice = (f) => (x) => f(f(x));

const plusThree = (i) => i + 3;

console.log(doTwice(plusThree)(7))  // 13
```

上面這個例子中，`doTwice` 就是一個既接收 function 作為參數，又 return 一個 function 的 HOF。

在 JavaScript 中，`Array` prototype 也有很多專屬的 higher-order methods，比如 `filter`：

```JavaScript
const arr = [2, 5, 1, 5, 3, 7, 3]
const biggerThanThree = arr.filter(num => num > 3)
console.log(biggerThanThree)  // [5, 5, 7]
```

如果要自己實作 `filter` 的話呢：

```JavaScript
function filter(iterable, predicate) {
    const result = [];
    for (let t of iterable) if (predicate(t)) result.push(t);
    return result;
}

const arr = [2, 5, 1, 5, 3, 7, 3]
const biggerThanThree = filter(arr, num => num > 3)
console.log(biggerThanThree)  // [5, 5, 7]
```

# Predicate & Functor

在上方自己實作 `filter` 的例子中，我們定義了一個叫做 `predicate` 的參數，該參數是一個回傳 boolean 的 function，而它事實上也對應到了 JavaScript 原生的 `filter` 所接收的的第一個參數。

針對一個可迭代物件，若我想對其中的每個元素進行一些運算，同時我可以將運算的過程寫成一個函式 $f$，則此時 $f$ 被稱為是一個 **functor**。

**Predicate** 則泛指回傳值為 boolean 的 functor，或者較鬆散的定義是：只要一個 functor 的回傳值可以被 implicitly converted 為 boolean，那它就算是一個 predicate。

# First-Class Citizen

在一個程式語言中，若 function 符合以下幾個條件，則可說該語言中的 function 為 first-class citizens（一等公民）：

- Function 可以被當作參數放進另一個 function
- Function 可以作為另一個 function 的 return value
- 可以 assign function 給一個變數

我們再看一次開頭的 `doTwice` function 範例，這次我們多做一個 assign function to variable 的動作：

```JavaScript
const doTwice = (f) => (x) => f(f(x));

const plusThree = (i) => i + 3;

const plusSix = doTwice(plusThree)

console.log(plusSix(7))  // 13
```

# 參考資料

- <https://ithelp.ithome.com.tw/articles/10235555>
